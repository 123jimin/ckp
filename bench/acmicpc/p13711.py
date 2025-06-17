from ckp.misc.lis import lis

import random
N = 1_000_000

A = []
B = []
iB = []
iBA = []

def setup():
    global A, B, iB, iBA

    random.seed(42)
    A, B = list(range(N)), list(range(N))
    random.shuffle(A); random.shuffle(B)

    iB = [0] * N
    for i, b in enumerate(B): iB[b] = i

    iBA = [iB[a] for a in A]

def bench():
    ans = len(lis(iBA))
    assert(ans == 2000)
    return ans

tags = {'lis'}