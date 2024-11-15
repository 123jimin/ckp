import random, operator, unittest

class DataGenerator:
    __slots__ = ('N', 'ops')

    N: int
    ops: list[str]

    def __init__(self, N: int, ops: list[str]):
        self.N = N
        self.ops = ops

    def index(self) -> int:
        return random.randrange(0, self.N)

    def range(self) -> tuple[int, int]:
        i = random.randrange(0, self.N)
        j = random.randrange(i, self.N+1)

        return (i, j)
    
    def value(self) -> int:
        return random.randint(-100, 100)
    
    def list(self) -> list[int]:
        return [self.value() for _ in range(self.N)]

    def op(self):
        match random.choice(self.ops):
            case 'get': return ('get', self.index())
            case 'sum_range': return ('sum_range', *self.range())
            case 'sum_all': return ('sum_all',)
            case 'set': return ('set', self.index(), self.value())
            case 'set_range': return ('set_range', *self.range(), self.value())
            case 'add_to': return ('add_to', self.index(), self.value())
            case 'add_to_range': return ('add_to_range', *self.range(), self.value())
    
    @staticmethod
    def test(asserter: unittest.TestCase, N: int, amount: int, test_ops: list, test_tree_maker, ref_tree_maker = None):
        gen = DataGenerator(N, test_ops)
        init_values = gen.list()

        test_tree = test_tree_maker(init_values)
        asserter.assertEqual(len(test_tree), N)

        ref_tree = (ref_tree_maker or NaiveSegmentTree)(init_values)
        for _ in range(amount):
            op = gen.op()
            match op:
                case ('get', i):
                    asserter.assertEqual(test_tree[i], ref_tree[i], f"{op=}")
                case ('sum_range', i, j):
                    asserter.assertEqual(test_tree.sum_range(i, j), ref_tree.sum_range(i, j), f"{op=}")
                case ('sum_all',):
                    asserter.assertEqual(test_tree.sum_all(), ref_tree.sum_all(), f"{op=}")
                case ('set', i, v):
                    test_tree[i] = v; ref_tree[i] = v
                case ('set_range', i, j, v):
                    test_tree.set_range(i, j, v); ref_tree.set_range(i, j, v)
                case ('add_to', i, v):
                    test_tree.add_to(i, v); ref_tree.add_to(i, v)
                case ('add_to_range', i, j, v):
                    test_tree.add_to_range(i, j, v); ref_tree.add_to_range(i, j, v)

class NaiveMonoidSegmentTree:
    __slots__ = ('_values', '_op', '_zero')

    def __init__(self, init_values, op, zero):
        self._values = init_values
        self._op = op
        self._zero = zero
    
    def __len__(self) -> int: return len(self._values)
    def __str__(self) -> str: return str(self._values)
    def __iter__(self): return self._values.__iter__()

    def __getitem__(self, ind: int): return self._values[ind]
    def sum_range(self, start: int, end: int):
        if start >= end: return self._zero
        v = self._values[start]
        for i in range(start+1, end): v = self._op(v, self._values[i])
        return v
    def sum_all(self): return self.sum_range(0, len(self._values))

    def __setitem__(self, ind: int, value): self._values[ind] = value
    def set_range(self, start: int, end: int, value):
        for i in range(start, end): self._values[i] = value

    def add_to(self, ind: int, value): self._values[ind] = self._op(self._values[ind], value)
    def add_to_range(self, start: int, end: int, value):
        for i in range(start, end): self._values[i] = self._op(self._values[i], value)

class NaiveSegmentTree(NaiveMonoidSegmentTree):
    def __init__(self, init_values: list[int]):
        super().__init__(init_values, operator.add, 0)