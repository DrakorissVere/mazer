import unittest

from main import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols)
        self.assertEqual(len(m1.cells), num_cols)
        self.assertEqual(len(m1.cells[0]), num_rows)

    def test_maze_start_and_end_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols)
        self.assertFalse(m1.cells[0][0].walls["left"])
        self.assertFalse(m1.cells[0][0].walls["top"])
        self.assertFalse(m1.cells[num_cols - 1][num_rows - 1].walls["right"])
        self.assertFalse(m1.cells[num_cols - 1][num_rows - 1].walls["bottom"])


if __name__ == '__main__':
    unittest.main()
