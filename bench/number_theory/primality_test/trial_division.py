from bench.util import bench
from ckp.number_theory.primality_test import is_prime, is_prime_trial_division, is_prime_trial_division_fast

def bench_normal():
    s = sum(map(is_prime, range(1, 1_000_001, 2)))
    assert(s == 78497)
    return s

def bench_trial():
    s = sum(map(is_prime_trial_division, range(1, 1_000_001, 2)))
    assert(s == 78497)
    return s

def bench_trial_fast():
    s = sum(map(is_prime_trial_division_fast, range(1, 1_000_001, 2)))
    assert(s == 78497)
    return s

def main():
    bench([
        bench_normal,
        bench_trial,
        bench_trial_fast,
    ], num_trials=10)

if __name__ == '__main__':
    main()