from tkinter import Tk, BOTH, Canvas
import time
import random

# x=0 is the left side of the screen
# y=0 is the top of the screen

CELL_SIZE = 40
CANVAS_PADDING = 20
BG_COLOR = "#272822"
WALL_COLOR = "white"


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def draw(self, canvas, fill_color="white"):
        canvas.create_line(self.a.x, self.a.y, self.b.x,
                           self.b.y, fill=fill_color, width=2)
        canvas.pack(fill=BOTH, expand=1)


class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("a-mazer")
        self.canvas = Canvas(self.root, width=width,
                             height=height, bg=BG_COLOR)
        self.canvas.pack(fill=BOTH, expand=1)
        self.is_running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()

    def close(self):
        self.is_running = False

    def draw_line(self, line, fill_color=WALL_COLOR):
        line.draw(self.canvas, fill_color)


class Cell:
    def __init__(self, pos, window=None):
        self.pos = pos
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False
        self._window = window

    def draw(self):
        if not self._window:
            return
        x = self.pos.x * CELL_SIZE + CANVAS_PADDING
        y = self.pos.y * CELL_SIZE + CANVAS_PADDING
        if self.walls["top"]:
            self._window.draw_line(Line(Point(x, y), Point(x + CELL_SIZE, y)))
        else:
            self._window.draw_line(
                Line(Point(x, y), Point(x + CELL_SIZE, y)), BG_COLOR)
        if self.walls["right"]:
            self._window.draw_line(
                Line(Point(x + CELL_SIZE, y), Point(x + CELL_SIZE, y + CELL_SIZE)))
        else:
            self._window.draw_line(
                Line(Point(x + CELL_SIZE, y), Point(x + CELL_SIZE, y + CELL_SIZE)), BG_COLOR)
        if self.walls["bottom"]:
            self._window.draw_line(
                Line(Point(x + CELL_SIZE, y + CELL_SIZE), Point(x, y + CELL_SIZE)))
        else:
            self._window.draw_line(
                Line(Point(x + CELL_SIZE, y + CELL_SIZE), Point(x, y + CELL_SIZE)), BG_COLOR)
        if self.walls["left"]:
            self._window.draw_line(Line(Point(x, y + CELL_SIZE), Point(x, y)))
        else:
            self._window.draw_line(
                Line(Point(x, y + CELL_SIZE), Point(x, y)), BG_COLOR)

    def draw_move(self, to_cell, undo=False):
        color = "black" if undo else "red"
        x = self.pos.x * CELL_SIZE + CANVAS_PADDING
        y = self.pos.y * CELL_SIZE + CANVAS_PADDING
        to_x = to_cell.pos.x * CELL_SIZE + CANVAS_PADDING
        to_y = to_cell.pos.y * CELL_SIZE + CANVAS_PADDING
        self._window.draw_line(Line(Point(x + CELL_SIZE / 2, y + CELL_SIZE / 2),
                                    Point(to_x + CELL_SIZE / 2, to_y + CELL_SIZE / 2)), color)


class Maze:
    def __init__(self, x, y, rows, cols, window=None, seed=None):
        self.start = Point(x, y)
        self.rows = rows
        self.cols = cols
        self._window = window
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self.cells = [[Cell(Point(x, y), self._window) for y in range(self.rows)]
                      for x in range(self.cols)]
        for i in range(self.rows):
            for j in range(self.cols):
                self._draw_cell(j, i)

    def _draw_cell(self, i, j):
        self.cells[i][j].draw()
        self._animate()

    def _animate(self):
        if not self._window:
            return
        self._window.redraw()
        time.sleep(0.001)

    def _break_entrance_and_exit(self):
        self.cells[0][0].walls["left"] = False
        self.cells[0][0].walls["top"] = False
        self._draw_cell(0, 0)
        self.cells[self.cols - 1][self.rows - 1].walls["right"] = False
        self.cells[self.cols - 1][self.rows - 1].walls["bottom"] = False
        self._draw_cell(self.cols - 1, self.rows - 1)

    def _break_walls_r(self, i, j):
        if i < 0 or i >= self.cols or j < 0 or j >= self.rows:
            return
        if self.cells[i][j].visited:
            return
        self.cells[i][j].visited = True
        self._draw_cell(i, j)
        neighbors = self._get_neighbors(i, j)
        random.shuffle(neighbors)
        for neighbor in neighbors:
            if not self.cells[neighbor[0]][neighbor[1]].visited:
                if neighbor[0] == i + 1:
                    self.cells[i][j].walls["right"] = False
                    self.cells[neighbor[0]][neighbor[1]].walls["left"] = False
                elif neighbor[0] == i - 1:
                    self.cells[i][j].walls["left"] = False
                    self.cells[neighbor[0]][neighbor[1]].walls["right"] = False
                elif neighbor[1] == j + 1:
                    self.cells[i][j].walls["bottom"] = False
                    self.cells[neighbor[0]][neighbor[1]].walls["top"] = False
                elif neighbor[1] == j - 1:
                    self.cells[i][j].walls["top"] = False
                    self.cells[neighbor[0]][neighbor[1]
                                            ].walls["bottom"] = False
                self._draw_cell(i, j)
                self._draw_cell(neighbor[0], neighbor[1])
                self._break_walls_r(neighbor[0], neighbor[1])

    def _get_neighbors(self, i, j):
        neighbors = []
        if i > 0:
            neighbors.append((i - 1, j))
        if i < self.cols - 1:
            neighbors.append((i + 1, j))
        if j > 0:
            neighbors.append((i, j - 1))
        if j < self.rows - 1:
            neighbors.append((i, j + 1))
        return neighbors

    def _reset_cells_visited(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].visited = False

    def _solve_r(self, i, j):
        self._animate()
        self.cells[i][j].visited = True
        if i == self.cols - 1 and j == self.rows - 1:
            return True
        # for each direction, if there is a cell and no wall blocking the way,
        # and cell hasn't been visited:
        # 1. draw a move between the current cell and that cell
        # 2. call _solve_r recursively to move to that cell. If that cell returns
        # True, just return True and don't worry about the other directions
        # 3. Otherwise, dran an "undo" move between the current cell and the next cell
        if i > 0 and not self.cells[i][j].walls["left"] and not self.cells[i - 1][j].visited:
            self.cells[i][j].draw_move(self.cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            self.cells[i][j].draw_move(self.cells[i - 1][j], True)
        if i < self.cols - 1 and not self.cells[i][j].walls["right"] and not self.cells[i + 1][j].visited:
            self.cells[i][j].draw_move(self.cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            self.cells[i][j].draw_move(self.cells[i + 1][j], True)
        if j > 0 and not self.cells[i][j].walls["top"] and not self.cells[i][j - 1].visited:
            self.cells[i][j].draw_move(self.cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            self.cells[i][j].draw_move(self.cells[i][j - 1], True)
        if j < self.rows - 1 and not self.cells[i][j].walls["bottom"] and not self.cells[i][j + 1].visited:
            self.cells[i][j].draw_move(self.cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            self.cells[i][j].draw_move(self.cells[i][j + 1], True)
        return False

    def solve(self):
        return self._solve_r(0, 0)


def main():
    window = Window(800, 600)
    cell_amount = 20
    maze = Maze(0, 0, cell_amount, cell_amount, window)
    maze.solve()
    window.wait_for_close()


if __name__ == '__main__':
    main()
