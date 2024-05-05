import unittest
from ckp.misc.sudoku import *

class TestSudoku(unittest.TestCase):
    def _check(self, init_arr):
        board = SudokuBoard.from_array(init_arr)

        board = SudokuBoard.solve(board)
        self.assertIsInstance(board, SudokuBoard)

        arr = board.to_array()
        self.assertEqual(len(arr), 9)

        for row, init_row in zip(arr, init_arr): 
            self.assertTrue(all(x in range(1, 10) for x in row))
            self.assertEqual(len(set(row)), 9)

            for x, init_x in zip(row, init_row):
                if init_x: self.assertEqual(x, init_x)

    def test(self):
        self._check([
            [0, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 3, 4, 6, 2, 0],
            [6, 0, 3, 0, 0, 0, 0, 7, 0],
            [0, 0, 0, 4, 8, 3, 5, 0, 7],
            [0, 0, 0, 0, 5, 0, 0, 6, 0],
            [0, 0, 0, 0, 0, 9, 0, 4, 0],
            [0, 0, 5, 0, 0, 0, 0, 0, 1],
            [8, 0, 0, 5, 4, 7, 3, 9, 6],
            [0, 0, 0, 0, 2, 1, 0, 0, 0],
        ])