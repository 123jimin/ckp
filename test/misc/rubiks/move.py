
import unittest
from ckp.misc.rubiks.move import *

class TestMove(unittest.TestCase):
    def test_inverse(self):
        for n in range(100):
            match n%4:
                case 0: pass
                case 1: self.assertEqual(inverse_move(n), n+2, f"{n=}")
                case 2: self.assertEqual(inverse_move(n), n, f"{n=}")
                case 3: self.assertEqual(inverse_move(n), n-2, f"{n=}")
    
    def test_to_str(self):
        self.assertEqual(move_to_str(1), "U")
        self.assertEqual(move_to_str(2), "U2")
        self.assertEqual(move_to_str(3), "U'")
        
        self.assertEqual(move_to_str(5), "F")
        self.assertEqual(move_to_str(6), "F2")
        self.assertEqual(move_to_str(7), "F'")
        
        self.assertEqual(move_to_str(9), "R")
        self.assertEqual(move_to_str(10), "R2")
        self.assertEqual(move_to_str(11), "R'")

        self.assertEqual(move_to_str(17), "D")
        self.assertEqual(move_to_str(18), "D2")
        self.assertEqual(move_to_str(19), "D'")
        
        self.assertEqual(move_to_str(21), "B")
        self.assertEqual(move_to_str(22), "B2")
        self.assertEqual(move_to_str(23), "B'")
        
        self.assertEqual(move_to_str(25), "L")
        self.assertEqual(move_to_str(26), "L2")
        self.assertEqual(move_to_str(27), "L'")

        self.assertEqual(moves_to_str([1, 3, 5, 7, 19, 18, 17, 11]), "UU'FF'D'D2DR'")
        self.assertEqual(moves_to_str([1, 17, 5, 21, 9, 25, 3, 19, 7, 23, 11, 27]), "UDFBRLU'D'F'B'R'L'")
    
    def test_to_move(self):
        for n in range(28):
            if n%4 == 0 or 12 <= n < 16: continue
            self.assertEqual(str_to_move(move_to_str(n)), n, f"{n=}")
    
    def test_to_moves(self):
        self.assertListEqual(str_to_moves("UFU'F'"), [1, 5, 3, 7])
        self.assertListEqual(str_to_moves("DB2L'UU"), [17, 22, 27, 1, 1])
        self.assertListEqual(str_to_moves("D, B2, L', UU"), [17, 22, 27, 1, 1])