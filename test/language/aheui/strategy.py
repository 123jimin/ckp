import unittest
from ckp.language.aheui.strategy import *
from ckp.language.aheui.simulate import aheui_run_strip

OPTIMAL_POS_INT_LEN = []
OPTIMAL_NEG_INT_LEN = []

class TestAheuiPushIntNaive(unittest.TestCase):
    def assertIdempotent(self, n: int):
        code = aheui_push_int_naive(n)
        output = aheui_run_strip(code + "망")

        self.assertEqual(output, str(n))
    
    def assertOptimal(self, n: int, optimal_len: int):
        code = aheui_push_int_naive(n)
        self.assertEqual(len(code), optimal_len, f"Suboptimal {code=} for {n=}")
    
    def test_idempotent(self):
        for n in range(-200, 201):
            self.assertIdempotent(n)
    
    def test_small_optimal(self):
        for i in range(1+aheui_push_int_naive.max_optimal):
            optimal_len = OPTIMAL_POS_INT_LEN[i]
            self.assertOptimal(i, optimal_len)

        for i in range(1-aheui_push_int_naive.min_optimal):
            optimal_len = OPTIMAL_NEG_INT_LEN[i]
            self.assertOptimal(-i, optimal_len)

class TestAheuiPushIntFromTrivial(unittest.TestCase):
    def test_idempotent(self):
        for top in range(-100, 101):
            push_top = aheui_push_int_naive(top)
            for n in range(-100, 101):
                code = aheui_push_int_from_trivial(top, n)
                if top == n: self.assertEqual(code, "", f"{top=} {n=} must return empty code")
                if code is None: continue

                output = aheui_run_strip(push_top+code+"망")
                self.assertEqual(output, str(n))

class TestAheuiPushIntFrom(unittest.TestCase):
    def assertIdempotent(self, top: int, value: int, effort: int):
        code = aheui_push_int_from(top, value, effort)
        output = aheui_run_strip(aheui_push_int_naive(top) + code + "망")

        self.assertEqual(output, str(value))

    def assertOptimal(self, top: int, value: int, effort: int, optimal_len: int):
        self.assertIdempotent(top, value, effort)

        code = aheui_push_int_from(top, value, effort)
        self.assertEqual(len(code), optimal_len, f"Suboptimal {code=} for {top=} {value=}")
    
    def test_optimal(self):
        self.assertOptimal(44, 111, 2, 4)

class TestAheuiFromVals(unittest.TestCase):
    def assertOptimal(self, input: str|list[int], optimal_len: int):
        if isinstance(input, str): input = list(input.encode('utf-8'))

        codes = aheui_from_vals(input)
        actual_len = sum(map(len, codes))

        self.assertEqual(actual_len, optimal_len, f"Suboptimal {codes=} for {input=}")
        output = aheui_run_strip("".join(f"{c}망발발다맣" for c in codes))
        
        self.assertEqual(output, "".join(f"{x}\n" for x in input), f"Different output for {input=}")

    def test_best_str(self):
        self.assertOptimal("Hello, world!", 43)
        self.assertOptimal("The quick brown fox jumps over the lazy dog.", 162)
        self.assertOptimal("다람쥐 헌 쳇바퀴에 타고파", 180)

    def test_optimal_dup(self):
        self.assertOptimal([32, 32], 4)
        self.assertOptimal([10, 100], 6)        

    @unittest.skip("stress test")
    def test_optimal_small_ints(self):
        for i in range(1+aheui_push_int_from.max_optimal):
            optimal_len = OPTIMAL_POS_INT_LEN[i]
            self.assertOptimal([i], optimal_len)

        for i in range(1-aheui_push_int_from.min_optimal):
            optimal_len = OPTIMAL_NEG_INT_LEN[i]
            self.assertOptimal([-i], optimal_len)
        

OPTIMAL_POS_INT_LEN = [
    3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5,
    3, 3, 5, 5, 3, 3, 5, 3, 3, 5, 3, 5, 3, 5, 5, 3, 3, 5, 5, 5,
    3, 5, 3, 5, 5, 3, 5, 5, 3, 3, 5, 5, 5, 5, 3, 5, 3, 5, 5, 5,
    5, 5, 5, 3, 3, 5, 5, 5, 5, 5, 5, 5, 3, 5, 5, 5, 5, 5, 5, 5,
    5, 3, 7, 5, 5, 5, 5, 5, 5, 5, 5, 5, 7, 7, 7, 7, 5, 7, 5, 5,

    5, 7, 5, 7, 5, 5, 7, 7, 5, 7, 7, 7, 5, 7, 7, 7, 7, 5, 7, 5,
    5, 5, 7, 7, 7, 5, 5, 7, 5, 7, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7,
    5, 7, 7, 7, 5, 7, 7, 5, 7, 7, 5, 7, 7, 5, 7, 7, 7, 7, 7, 7,
    5, 7, 5, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7,
    5, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 5, 7, 7, 7, 5, 7, 7, 7,

    5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 5, 7, 7, 7,
    7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    5, 7, 7, 5, 7, 5, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 5, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    5, 7, 7, 7, 7, 7, 7, 7, 5, 5, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7,

    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7,
    5, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7,
    7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9,
    5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 7,
    7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 7,

    5, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9,
    7, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 9, 5, 7, 7, 7, 7, 7, 7, 7,
    7, 5, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 7,
    7, 9, 7, 9, 7, 9, 9, 9, 7, 7, 9, 9, 7, 9, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 9, 5, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,

    7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 7, 5, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 9, 9, 7, 9, 9, 7, 7, 9, 7, 7, 7, 7, 9, 7, 9, 9, 7,
    7, 9, 9, 9, 7, 9, 7, 9, 9, 7, 7, 9, 7, 7, 9, 9, 9, 9, 7, 7,
    7, 7, 7, 7, 7, 7, 9, 5, 7, 7, 7, 7, 7, 7, 7, 7, 5, 9, 7, 7,
    7, 7, 7, 7, 7, 7, 9, 9, 7, 9, 9, 9, 7, 9, 7, 7, 9, 9, 9, 9,

    7, 9, 7, 7, 9, 7, 9, 9, 7, 7, 9, 9, 7, 9, 9, 9, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 5, 9, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 7, 9, 7,
    7, 7, 7, 7, 7, 7, 7, 9, 5, 9, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9,
    7, 7, 9, 9, 7, 9, 7, 9, 9, 9, 9, 9, 7, 9, 9, 7, 7, 9, 9, 9,
    7, 9, 7, 9, 7, 9, 7, 9, 7, 9, 7, 9, 9, 7, 9, 9, 7, 9, 9, 9,

    7, 9, 7, 9, 7, 9, 9, 9, 9, 9, 9, 7, 7, 9, 7, 9, 9, 9, 9, 9,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 9, 7, 7, 7, 7, 7, 7, 7, 7, 9,
    7, 9, 9, 9, 7, 9, 9, 7, 9, 9, 7, 9, 9, 9, 9, 9, 7, 9, 9, 9,
    9, 9, 9, 9, 9, 7, 9, 9, 7, 9, 9, 9, 9, 9, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 5, 9, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9, 9,

    7, 7, 9, 9, 9, 9, 9, 9, 9, 9, 7, 9, 7, 9, 9, 9, 7, 9, 9, 7,
    7, 9, 9, 9, 9, 7, 9, 9, 9, 9, 9, 9, 7, 7, 9, 9, 9, 7, 9, 9,
    7, 7, 9, 9, 9, 7, 9, 7, 9, 9, 7, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    9, 9, 9, 9, 7, 9, 9, 7, 7, 9, 8, 9, 9, 9, 9, 7, 9, 9, 9, 9,
    9, 9, 7, 9, 9, 9, 9, 9, 9, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 9,

    5, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9, 9, 9, 7, 9,
    9, 9, 9, 9, 7, 9, 9, 9, 7, 9, 7, 9, 9, 9, 9, 9, 7, 7, 9, 9,
    9, 9, 9, 9, 9, 7, 9, 9, 9, 9, 9, 9, 7, 9, 9, 9, 9, 9, 9, 9,
    7, 7, 9, 9, 9, 9, 9, 9, 7, 9, 9, 9, 7, 9, 9, 9, 9, 9, 9, 9,
    7, 9, 9, 9, 9, 9, 9, 9, 9, 9, 7, 9, 7, 9, 9, 9, 9, 9, 9, 9,

    7,
]

OPTIMAL_NEG_INT_LEN = [
    3, 3, 3, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 7, 5, 5, 5, 5, 5, 5, 5, 5,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,

    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9,

    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 9, 9, 7, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 7, 7, 7, 7, 9, 9,

    7, 7, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 9, 7, 7, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 9, 9, 7, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9,
    7, 9, 9, 9, 7, 7, 7, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,

    7, 7, 7, 7, 9, 7, 7, 9, 7, 9, 9, 9, 9, 7, 7, 9, 7, 9, 9, 9,
    7, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 9, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 9, 7, 9, 7, 9, 9, 9, 9, 7, 7, 9, 9, 7,
    9, 9, 7, 9, 7, 9, 9, 9, 7, 7, 9, 9, 7, 9, 7, 8, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 9, 7, 9, 7, 9, 7, 9, 9, 9, 9, 7, 7, 7, 7, 7,

    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 7, 9,
    7, 9, 7, 9, 9, 7, 9, 9, 7, 9, 9, 7, 7, 9, 9, 9, 7, 9, 9, 7,
    7, 9, 9, 9, 7, 9, 7, 9, 9, 7, 8, 9, 7, 7, 9, 9, 9, 9, 7, 7,
    7, 7, 7, 7, 7, 7, 9, 7, 7, 7, 7, 7, 7, 7, 7, 8, 7, 9, 9, 9,
    9, 9, 9, 9, 7, 7, 9, 9, 8, 9, 9, 9, 7, 9, 7, 9, 9, 9, 9, 9,

    7, 9, 9, 7, 9, 9, 9, 9, 7, 9, 9, 9, 7, 9, 9, 9, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 9, 9, 9, 9, 9, 7, 9, 7, 9, 9, 9, 9, 9, 9, 7,
    7, 7, 7, 7, 7, 7, 7, 9, 7, 9, 9, 9, 9, 9, 9, 9, 9, 7, 9, 9,
    8, 9, 9, 9, 9, 9, 7, 9, 9, 9, 9, 9, 8, 9, 9, 7, 9, 9, 9, 9,
    9, 9, 9, 9, 7, 9, 9, 9, 9, 9, 8, 9, 9, 7, 9, 9, 9, 9, 9, 9,

    8, 9, 7, 9, 9, 9, 9, 9, 9, 9, 9, 7, 9, 9, 9, 9, 9, 9, 9, 9,
    7, 7, 7, 7, 7, 7, 7, 7, 8, 9, 9, 9, 9, 9, 9, 9, 8, 9, 9, 9,
    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 9, 9, 9, 9, 9, 7, 9, 9, 9,
    9, 9, 9, 9, 9, 9, 9, 9, 8, 9, 9, 9, 9, 9, 9, 7, 7, 7, 7, 7,
    7, 7, 7, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,

    8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 9, 9, 9, 9, 9, 9, 9,
    8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 11, 9, 9, 9, 9, 9, 9,
    9, 9, 9, 9, 8, 9, 9, 9, 9, 9, 7, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 9,

    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    9, 9, 9, 9, 9, 9, 9, 9, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    9, 9, 9, 9, 9, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 9, 9, 9, 9, 9, 9, 9,
    8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 7, 9, 9, 9, 9, 9, 9, 9,
]