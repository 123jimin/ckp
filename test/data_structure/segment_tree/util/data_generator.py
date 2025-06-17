from typing import Callable, Any, List
import random, unittest

from ckp.data_structure.segment_tree.naive import NaiveSegmentTree

class TestDataGenerator:
    __slots__ = ('N', 'ops', 'generate_value')

    N: int
    """ Size of the tree. """

    ops: list[str]
    """ List of names of methods to test. """

    generate_value: Callable[[], Any]
    """ Function that generates a random value. """

    def __init__(self, N: int, ops: list[str], generate_value: Callable[[], Any]):
        self.N = N
        self.ops = ops
        self.generate_value = generate_value
    
    def op(self):
        """ Returns a random segment tree operation. """
        match random.choice(self.ops):
            case 'get': return ('get', self.index())
            case 'sum_range': return ('sum_range', *self.range())
            case 'sum_all': return ('sum_all',)
            case 'set': return ('set', self.index(), self.value())
            case 'set_range': return ('set_range', *self.range(), self.value())
            case 'add_to': return ('add_to', self.index(), self.value())
            case 'add_to_range': return ('add_to_range', *self.range(), self.value())
            case 'mul_to': return ('mul_to', self.index(), self.value())
            case 'mul_to_range': return ('mul_to_range', *self.range(), self.value())
            case 'mul_add_to': return ('mul_add_to', self.index(), self.value(), self.value())
            case 'mul_add_to_range': return ('mul_add_to_range', *self.range(), self.value(), self.value())
            case _: raise ValueError(f"Unknown operation: {self.ops}")
    
    def index(self) -> int:
        return random.randrange(0, self.N)

    def range(self) -> tuple[int, int]:
        l = random.randint(0, self.N)
        start = random.randint(0, self.N-l)
        return (start, start+l)
    
    def value(self):
        return self.generate_value()
    
    def list(self) -> list:
        """ Returns a list of values, that can be used for initializing a segment tree. """
        return [self.value() for _ in range(self.N)]

    @staticmethod    
    def bench(tree, ops):
        """ Benchmarks the given segment tree with the given operations. """
        for op in ops:
            match op:
                case ('get', i): tree[i]
                case ('sum_range', i, j): tree.sum_range(i, j)
                case ('sum_all',): tree.sum_all()

                case ('set', i, v): tree[i] = v
                case ('set_range', i, j, v): tree.set_range(i, j, v)

                case ('add_to', i, v): tree.add_to(i, v)
                case ('add_to_range', i, j, v): tree.add_to_range(i, j, v)

                case ('mul_to', i, v): tree.mul_to(i, v)
                case ('mul_to_range', i, j, v): tree.mul_to_range(i, j, v)

                case ('mul_add_to', i, v1, v2): tree.mul_add_to(i, v1, v2)
                case ('mul_add_to_range', i, j, v1, v2): tree.mul_add_to_range(i, j, v1, v2)

    @staticmethod
    def test(
        asserter: unittest.TestCase, N: int, amount: int, test_ops: List[str],
        test_tree_maker, ref_tree_maker=None, *,
        value_generator: Callable[[], Any] = lambda: random.randint(-100, 100)
    ):
        gen = TestDataGenerator(N, test_ops, value_generator)
        init_values = gen.list()

        test_tree = test_tree_maker(init_values)
        asserter.assertEqual(len(test_tree), N)

        ref_tree = (ref_tree_maker or NaiveSegmentTree)(init_values)

        for _ in range(amount):
            match (op := gen.op()):
                case ('get', i): asserter.assertEqual(test_tree[i], ref_tree[i], f"{op=}")
                case ('sum_range', i, j): asserter.assertEqual(test_tree.sum_range(i, j), ref_tree.sum_range(i, j), f"{op=}")
                case ('sum_all',): asserter.assertEqual(test_tree.sum_all(), ref_tree.sum_all(), f"{op=}")
                
                case ('set', i, v): test_tree[i] = v; ref_tree[i] = v
                case ('set_range', i, j, v): test_tree.set_range(i, j, v); ref_tree.set_range(i, j, v)

                case ('add_to', i, v): test_tree.add_to(i, v); ref_tree.add_to(i, v)
                case ('add_to_range', i, j, v): test_tree.add_to_range(i, j, v); ref_tree.add_to_range(i, j, v)
                
                case ('mul_to', i, v): test_tree.mul_to(i, v); ref_tree.mul_to(i, v)
                case ('mul_to_range', i, j, v): test_tree.mul_to_range(i, j, v); ref_tree.mul_to_range(i, j, v)

                case ('mul_add_to', i, m, d): test_tree.mul_add_to(i, m, d); ref_tree.mul_add_to(i, m, d)
                case ('mul_add_to_range', i, j, m, d): test_tree.mul_add_to_range(i, j, m, d); ref_tree.mul_add_to_range(i, j, m, d)
        
        asserter.assertListEqual(list(test_tree), list(ref_tree), "Final values")