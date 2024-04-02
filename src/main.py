from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("a-mazer")
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack()
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


def main():
    window = Window(800, 600)
    window.wait_for_close()


if __name__ == '__main__':
    main()
