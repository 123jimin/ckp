import unittest
from ckp.language.aheui import *
from ckp.language.aheui.simulate import aheui_run_strip

class TestAheuiFromText(unittest.TestCase):
    def assertIdempotent(self, text: str):
        code = aheui_from_text(text)
        output = aheui_run_strip(code)

        self.assertEqual(output, text)

    def test_simple(self):
        self.assertIdempotent("")
        self.assertIdempotent("1234 + 5678 = ?")
        self.assertIdempotent("Hello, world!\n")
        self.assertIdempotent("The quick brown fox jumps over the lazy dog.\n")
    
    def test_int(self):
        for i in range(-200, 201):
            self.assertIdempotent(str(i))

class TestAheuiFromVals(unittest.TestCase):
    def assertOptimal(self, input: list[int], optimal_len: int):
        codes = aheui_from_vals(input)
        actual_len = sum(map(len, codes))

        self.assertEqual(actual_len, optimal_len, f"Suboptimal for {input=}")
        output = aheui_run_strip("".join(f"{c}망발발다맣" for c in codes))
        
        self.assertEqual(output, "".join(f"{x}\n" for x in input), f"Different output for {input=}")

    def test_optimal_dup(self):
        self.assertOptimal([32, 32], 4)
        self.assertOptimal([10, 100], 6)        

    def test_optimal_small_ints(self):
        OPTIMAL_LEN = [
            3, 3, 1, 1, 1, 1, 1, 1, 1, 1,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 5,
            3, 3, 5, 5, 3, 3, 5, 3, 3, 5,
            3, 5, 3, 5, 5, 3, 3, 5, 5, 5,
            3, 5, 3, 5, 5, 3, 5, 5, 3, 3,
            5, 5, 5, 5, 3, 5, 3, 5, 5, 5,
            5, 5, 5, 3, 3, 5, 5, 5, 5, 5,
            5, 5, 3, 5, 5, 5, 5, 5, 5, 5,
            5, 3, 7, 5, 5, 5, 5, 5, 5, 5,
            5, 5, 7, 7, 7, 7, 5, 7, 5, 5,
            5, 7, 5, 7, 5, 5, 7, 7, 5, 7,
            7, 7, 5, 7, 7, 7, 7, 5, 7, 5,
            5, 7, 7, 7, 7, 5, 5, 7, 5, 7,
            7, 7, 7, 7, 7, 5, 5, 7, 7, 7,
            5, 7, 7, 7, 5, 7, 7, 5, 7, 7,
            5, 7, 7, 5, 7, 7, 7, 7, 7, 7,
            5, 7, 5, 7, 7, 7, 7, 7, 5, 7,
            7, 7, 7, 7, 7, 5, 7, 7, 7, 7,
            5, 7, 7, 7, 7, 7, 7, 7, 7, 5,
            7, 7, 5, 7, 7, 7, 5, 7, 7, 7,
        ]
        for i, optimal_len in enumerate(OPTIMAL_LEN):
            self.assertOptimal([i], optimal_len)