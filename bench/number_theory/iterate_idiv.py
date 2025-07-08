from bench.util import bench

from ckp.number_theory.misc import iterate_idiv

def iterate_idiv_new(x: int):
    yield(x, 1, 2)

    if x <= 3:
        if x == 2: yield (1, 2, 3)
        elif x == 3: yield (1, 2, 4)
        return
    
    prev_q = x//2
    
    for i in range(3, x+1):
        if (q := x//i) == prev_q: break
        yield (prev_q, i-1, i)
        prev_q = q
    
    i -= 1
    
    for q in range(prev_q, 1, -1):
        next_i = x//q + 1
        yield (q, i, next_i)
        i = next_i
    
    yield(1, i, x+1)

def bench_idiv():
    s = 0
    for (q, i, j) in iterate_idiv(10**13):
        s += (q*q)*(j-i)
    return s

def bench_idiv_new():
    s = 0
    for (q, i, j) in iterate_idiv_new(10**13):
        s += (q*q)*(j-i)
    return s

def bench_idiv_manual():
    s = 0
    i = 1
    x = 10**13
    while i <= x:
        q = x // i
        j = x // q + 1
        s += (q*q)*(j-i)
        i = j
    return s

if __name__ == '__main__':
    bench([
        bench_idiv,
        bench_idiv_new,
        bench_idiv_manual,
    ], num_trials=5)