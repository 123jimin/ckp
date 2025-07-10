from bench.util import bench
from ckp.number_theory.factor import *

import math, cProfile

def pollard_rho_find_divisor_simple1(n: int, start: int = 2):
    g = math.gcd
    if 1 < (d := g(n, start)) < n: return d

    l = [x:=start*start%n+1]
    for p in l:
        if (d := g((y:=x*x%n+1) - p, n)) != 1: return 0 if d == n else d
        l += (y, x:=y*y%n+1)

def pollard_rho_find_divisor_simple2(n: int, start: int = 2):
    g = math.gcd
    if 1 < (d := g(n, start)) < n: return d

    x = y = start
    p = 1
    while True:
        for _ in range(p):
            y = y*y%n + 1
            if (d := g(x-y, n)) != 1:
                return 0 if d == n else d
        x = y
        p += p

def pollard_rho_find_divisor_alt(n:int, start:int = 2):
    g = math.gcd
    if 1 < (d := g(n, start)) < n: return d

    x = start

    # Doing `y*y % n` is 10% faster than using `pow(y, 2, n)`.
    x1 = x*x%n + 1
    if (d := g((x2 := x1*x1%n + 1) - x1, n)) != 1: return 0 if d == n else d

    x3 = x2*x2%n + 1
    if (d := g((x4 := x3*x3%n + 1) - x2, n)) != 1: return 0 if d == n else d

    x5 = x4*x4%n + 1
    if (d := g((x6 := x5*x5%n + 1) - x3, n)) != 1: return 0 if d == n else d
    
    x7 = x6*x6%n + 1
    if (d := g((x8 := x7*x7%n + 1) - x4, n)) != 1: return 0 if d == n else d

    # Memory usage incurred by storing past trajectory isn't a big deal in practice.
    # Also, pre-allocating `l` doesn't seem to affect overall performance.
    i, i4, l = 0, 4, [x5, x6, x7, x8]
    while True:
        p0, p1, p2, p3 = l[i:i4]
        x1 = x8*x8%n + 1
        if (d := g((x2 := x1*x1%n + 1) - p0, n)) != 1: return 0 if d == n else d

        x3 = x2*x2%n + 1
        if (d := g((x4 := x3*x3%n + 1) - p1, n)) != 1: return 0 if d == n else d

        x5 = x4*x4%n + 1
        if (d := g((x6 := x5*x5%n + 1) - p2, n)) != 1: return 0 if d == n else d
        
        x7 = x6*x6%n + 1
        if (d := g((x8 := x7*x7%n + 1) - p3, n)) != 1: return 0 if d == n else d

        l += (x1, x2, x3, x4, x5, x6, x7, x8)
        i, i4 = i4, i4 + 4

def bench_find_divisor():
    # A random prime number, chosen by a fair dice roll.
    p = 1854622803871
    x = pollard_rho_find_divisor(p ** 2)
    assert x == p
    return x

def bench_find_divisor_simple1():
    p = 1854622803871
    x = pollard_rho_find_divisor_simple1(p ** 2)
    assert x == p
    return x

def bench_find_divisor_simple2():
    p = 1854622803871
    x = pollard_rho_find_divisor_simple2(p ** 2)
    assert x == p
    return x

def bench_find_divisor_alt():
    p = 1854622803871
    x = pollard_rho_find_divisor_alt(p ** 2)
    assert x == p
    return x

def bench_factor():
    x = sum(max(factor_pollard_rho(r)) for r in range(1_000_000_000, 1_000_010_000))
    assert x == 823444990958
    return x

if __name__ == '__main__':
    bench([
        bench_find_divisor,
        bench_find_divisor_alt,
        bench_find_divisor_simple1,
        bench_find_divisor_simple2,
    ], num_trials=5)

    cProfile.runctx("for _ in range(10): f()", {'f': bench_find_divisor}, {}, sort='tottime')