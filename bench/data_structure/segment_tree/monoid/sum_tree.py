from bench.util import bench
from ckp.data_structure.segment_tree import SumSegmentTree, AbstractSumSegmentTree
from test.data_structure.segment_tree.util.data_generator import TestDataGenerator
import cProfile

class SumSegmentTreeAlt(AbstractSumSegmentTree):
    """ Segment tree for summing numbers in ranges. """

    __slots__ = ()
    
    def __init__(self, init_values: list|int):
        """ Creates a segment tree on `init_values`. """
        is_init_list = not isinstance(init_values, int)

        L = self._len = len(init_values) if is_init_list else init_values
        if not L: self._tree = []; return
    
        tree = self._tree = [0] * L + init_values if is_init_list else [0] * (L+L)

        for i in range(L-1, 0, -1):
            i2 = i+i; tree[i] = tree[i2] + tree[i2+1]
    
    def sum_range(self, start: int, end: int):
        """ Get the sum of elements at indices in the half-open range [start, end). """
        tree, L = self._tree, self._len
        
        if start >= 0: start += L
        else: start = L

        if end < L: end += L
        else: end = L+L

        res = 0

        while start < end:
            if start & 1: res += tree[start]; start += 1
            if end & 1: res += tree[end - 1]
            start //= 2; end //= 2
        
        return res
    
    def sum_all(self):
        """ Get the sum of all elements in this tree. """
        return self._tree[1] if self._len else 0
    
    def __setitem__(self, ind: int, value):
        if not 0 <= ind < self._len:
            raise IndexError(f"Index {ind} out of range (len={self._len})")
        
        curr_ind, tree = self._len + ind, self._tree
        if not (delta := value - tree[curr_ind]): return

        tree[curr_ind] = value
        while curr_ind > 1: tree[curr_ind := curr_ind//2] += delta

    def add_to(self, ind: int, value):
        """ Add a given value to (the right side of) `self[ind]`. """
        if not 0 <= ind < self._len:
            raise IndexError(f"Index {ind} out of range (len={self._len})")
        
        curr_ind, tree = self._len + ind, self._tree
        tree[curr_ind] += value

        while curr_ind > 1: tree[curr_ind := curr_ind // 2] += value

import random
random.seed(42)

N, Q = 100_000, 100_000

data_gen = TestDataGenerator(N,  ['set', 'sum_range', 'get'], lambda: random.randint(-100, 100))
init_values = data_gen.list()
ops = [data_gen.op() for _ in range(Q)]

def bench_sum():
    res = TestDataGenerator.bench(SumSegmentTree(init_values), ops)
    assert(sum(res) == 327828661)

def bench_alt():
    res = TestDataGenerator.bench(SumSegmentTreeAlt(init_values), ops)
    assert(sum(res) == 327828661)

if __name__ == "__main__":
    bench([
        bench_sum,
        bench_alt,
    ], num_trials=10)

    cProfile.runctx("for _ in range(10): f()", {'f': bench_alt}, {}, sort='tottime')