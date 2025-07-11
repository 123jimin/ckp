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
        self.assertIdempotent("Hello, world!")
        self.assertIdempotent("The quick brown fox jumps over the lazy dog.")
    
    @unittest.skip("stress test")
    def test_hangul(self):
        self.assertIdempotent("키스의 고유 조건은 입술끼리 만나야 하고 특별한 기술은 필요치 않다.")
    
    def test_int(self):
        for i in range(-200, 201):
            self.assertIdempotent(str(i))