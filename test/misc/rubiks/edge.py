import unittest
from ckp.misc.rubiks.edge import *
from ckp.misc.rubiks.move import str_to_move, str_to_moves

def make_move_pairs(m: int):
    for i in (1, 2, 3):
        for j in (1, 2, 3):
            x = (i+j) % 4
            if x: yield ([m+i, m+j], [m+x])
            else: yield ([m+i, m+j], [])

class TestEdgeTurn(unittest.TestCase):
    def test_face_clockwise(self):
        init_state = edge_init()

        self.assertTupleEqual(edge_turn(init_state, str_to_move("U")), (1, 2, 3, 0, 4, 5, 6, 7, 8, 9, 10, 11), "move U")
        self.assertTupleEqual(edge_turn(init_state, str_to_move("D")), (0, 1, 2, 3, 4, 5, 6, 7, 11, 8, 9, 10), "move D")

        self.assertTupleEqual(edge_turn(init_state, str_to_move("F")), (23, 1, 2, 3, 16, 5, 6, 24, 20, 9, 10, 11), "move F")
        self.assertTupleEqual(edge_turn(init_state, str_to_move("B")), (0, 1, 21, 3, 4, 26, 18, 7, 8, 9, 22, 11), "move B")
        
        self.assertTupleEqual(edge_turn(init_state, str_to_move("R")), (0, 4, 2, 3, 9, 1, 6, 7, 8, 5, 10, 11), "move R")
        self.assertTupleEqual(edge_turn(init_state, str_to_move("L")), (0, 1, 2, 6, 4, 5, 11, 3, 8, 9, 10, 7), "move L")

    def test_same_layer(self):
        init_state = edge_init()
        for m in (0, 4, 8, 16, 20, 24):
            for v1, v2 in make_move_pairs(m):
                state1 = state2 = init_state
                for v in v1: state1 = edge_turn(state1, v)
                for v in v2: state2 = edge_turn(state2, v)
                self.assertTupleEqual(state1, state2, f"{v1=} {v2=}")

    def test_invariant(self):
        init_state = edge_init()
        for m in (0, 4, 8, 16, 20, 24):
            for move in (m+1, m+2, m+3):
                state = edge_turn(init_state, move)

                self.assertTrue(all(0 <= s < 12 or 16 <= s < 32 for s in state), f"{move=} {state=} state int range")
                self.assertSetEqual(set(s%16 for s in state), {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}, f"{move=} {state=} state position")
                self.assertEqual(sum(s//16 for s in state)%2, 0, f"{move=} {state=} state orientation")