import unittest
from ckp.language.aheui.from_text import *
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