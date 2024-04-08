from tkinter import Tk, BOTH, Canvas
import time

# x=0 is the left side of the screen
# y=0 is the top of the screen

CELL_SIZE = 40
CANVAS_PADDING = 20


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
                             height=height, bg="#272822")
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

    def draw_line(self, line, fill_color="white"):
        line.draw(self.canvas, fill_color)


class Cell:
    def __init__(self, pos, window=None):
        self.pos = pos
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self._window = window

    def draw(self):
        if not self._window:
            return
        x = self.pos.x * CELL_SIZE + CANVAS_PADDING
        y = self.pos.y * CELL_SIZE + CANVAS_PADDING
        if self.walls["top"]:
            self._window.draw_line(Line(Point(x, y), Point(x + CELL_SIZE, y)))
        if self.walls["right"]:
            self._window.draw_line(
                Line(Point(x + CELL_SIZE, y), Point(x + CELL_SIZE, y + CELL_SIZE)))
        if self.walls["bottom"]:
            self._window.draw_line(
                Line(Point(x + CELL_SIZE, y + CELL_SIZE), Point(x, y + CELL_SIZE)))
        if self.walls["left"]:
            self._window.draw_line(Line(Point(x, y + CELL_SIZE), Point(x, y)))

    def draw_move(self, to_cell, undo=False):
        color = "red" if undo else "gray"
        x = self.pos.x * CELL_SIZE + CANVAS_PADDING
        y = self.pos.y * CELL_SIZE + CANVAS_PADDING
        to_x = to_cell.pos.x * CELL_SIZE + CANVAS_PADDING
        to_y = to_cell.pos.y * CELL_SIZE + CANVAS_PADDING
        self._window.draw_line(Line(Point(x + CELL_SIZE / 2, y + CELL_SIZE / 2),
                                    Point(to_x + CELL_SIZE / 2, to_y + CELL_SIZE / 2)), color)


class Maze:
    def __init__(self, x, y, rows, cols, window=None):
        self.start = Point(x, y)
        self.rows = rows
        self.cols = cols
        self._window = window
        self._create_cells()

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
        time.sleep(0.01)


def main():
    window = Window(800, 600)
    cell_amount = 20
    maze = Maze(0, 0, cell_amount, cell_amount, window)
    window.wait_for_close()


if __name__ == '__main__':
    main()
