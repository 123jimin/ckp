
import unittest
from ckp.misc.rubiks.corner import *
from ckp.misc.rubiks.move import str_to_move, str_to_moves

def make_move_pairs(m: int):
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            x = (i+j) % 4
            if x: yield ([m+i, m+j], [m+x])
            else: yield ([m+i, m+j], [])

class TestCornerTurn(unittest.TestCase):
    def test_face_clockwise(self):
        init_state = corner_init()
        
        self.assertTupleEqual(corner_turn(init_state, str_to_move("U")), (1, 2, 3, 0, 4, 5, 6, 7), "move U")
        self.assertTupleEqual(corner_turn(init_state, str_to_move("D")), (0, 1, 2, 3, 7, 4, 5, 6), "move D")
        
        self.assertTupleEqual(corner_turn(init_state, str_to_move("F")), (11, 1, 2, 23, 16, 5, 6, 12), "move F")
        self.assertTupleEqual(corner_turn(init_state, str_to_move("B")), (0, 21, 9, 3, 4, 14, 18, 7), "move B")

        self.assertTupleEqual(corner_turn(init_state, str_to_move("R")), (20, 8, 2, 3, 13, 17, 6, 7), "move R")
        self.assertTupleEqual(corner_turn(init_state, str_to_move("L")), (0, 1, 22, 10, 4, 5, 15, 19), "move L")

    def test_same_layer(self):
        init_state = corner_init()
        for m in (0, 4, 8, 16, 20, 24):
            for v1, v2 in make_move_pairs(m):
                state1 = state2 = init_state
                for v in v1: state1 = corner_turn(state1, v)
                for v in v2: state2 = corner_turn(state2, v)
                self.assertTupleEqual(state1, state2, f"{v1=} {v2=}")
    
    def test_invariant(self):
        init_state = corner_init()
        for m in (0, 4, 8, 16, 20, 24):
            for move in (m+1, m+2, m+3):
                state = corner_turn(init_state, move)

                self.assertTrue(all(0 <= s < 24 for s in state), f"{move=} {state=} state int range")
                self.assertSetEqual(set(s%8 for s in state), {0, 1, 2, 3, 4, 5, 6, 7}, f"{move=} {state=} state position")
                self.assertEqual(sum(s//8 for s in state)%3, 0, f"{move=} {state=} state orientation")
    
    def test_pll(self):
        for (state, algorithm) in [((1, 0, 2, 3, 4, 5, 6, 7), "RUR'F'RUR'U'R'FR2U'R'")]:
            for move in str_to_moves(algorithm): state = corner_turn(state, move)
            self.assertTupleEqual(state, corner_turn(corner_init(), str_to_move("U")), f"{algorithm=}")