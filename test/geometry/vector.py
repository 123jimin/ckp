import unittest
from ckp.geometry.vector import *

class TestVec2(unittest.TestCase):
    def test_simple(self):
        a = Vec2(0, 1)
        b = Vec2(1, 0)
        z = Vec2(0, 0)

        self.assertTrue(a)
        self.assertTrue(b)
        self.assertFalse(z)

        self.assertEqual(a+a, Vec2(0, 2))
        self.assertEqual(b+b, Vec2(2, 0))
        self.assertEqual(a+b, Vec2(1, 1))

        self.assertEqual(a-a, z)
        self.assertEqual(b-b, z)
        self.assertEqual(a-b, Vec2(-1, 1))
        self.assertEqual(b-a, Vec2(1, -1))

        self.assertEqual(-a, Vec2(0, -1))
        self.assertEqual(-b, Vec2(-1, 0))
        self.assertEqual(-z, z)
        
        self.assertEqual(a+z, a)
        self.assertEqual(z+b, b)

        self.assertEqual(a*a, 1)
        self.assertEqual(a*b, 0)
        self.assertEqual(3*a, Vec2(0, 3))
        self.assertEqual(3*b, Vec2(3, 0))
        self.assertEqual((6*a - 5*b)*a, 6)

        self.assertGreater(z.orientation(b, a), 0)
        self.assertLess(z.orientation(a, b), 0)
        self.assertEqual(z.orientation(Vec2(1, 2), Vec2(3, 6)), 0)

class TestVec3(unittest.TestCase):
    def test_simple(self):
        i = Vec3(1, 0, 0)
        j = Vec3(0, 1, 0)
        k = Vec3(0, 0, 1)

        self.assertEqual(i @ j, k)
        self.assertEqual(j @ i, -k)