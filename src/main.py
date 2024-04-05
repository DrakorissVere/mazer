from tkinter import Tk, BOTH, Canvas

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
    def __init__(self, pos, window):
        self.pos = pos
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self._window = window

    def draw(self):
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


def main():
    window = Window(800, 600)
    cell_amount = 20
    cells = [[Cell(Point(x, y), window) for y in range(cell_amount)]
             for x in range(cell_amount)]
    for row in cells:
        for cell in row:
            cell.draw()
    cells[0][0].draw_move(cells[1][0])
    cells[1][0].draw_move(cells[1][1])
    cells[1][1].draw_move(cells[0][1], True)
    window.wait_for_close()


if __name__ == '__main__':
    main()
