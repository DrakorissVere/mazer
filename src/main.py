from tkinter import Tk, BOTH, Canvas

# x=0 is the left side of the screen
# y=0 is the top of the screen


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


def main():
    window = Window(800, 600)
    line = Line(Point(100, 100), Point(200, 200))
    window.draw_line(line)
    window.wait_for_close()


if __name__ == '__main__':
    main()
