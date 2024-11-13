"""
    Compare CKP's primality test with primality tests from different libraries.
"""

from bench.util import bench
from ckp.number_theory.primality_test import is_prime as is_prime_ckp

# External libraries for benchmarking
from primality.primality import isprime as is_prime_primality
from sympy.ntheory.primetest import isprime as is_prime_sympy

x = 0

def main():
    global x

    TEST_DATA: list[tuple[int, int, int]] = [
        (4, 7, 100_000),
        (6, 3, 100_000),
        (8, 7, 10_000),
        (9, 7, 10_000),
        (20, 39, 1000),
        (50, 151, 100),
        (200, 357, 10),
    ]

    for (k, d, repeat) in TEST_DATA:
        x = 10**k + d
        print(f"Testing: 10**{k}+{d} ({repeat} times)")
        bench([
            "is_prime_primality(x)",
            "is_prime_sympy(x)",
            "is_prime_ckp(x)",
        ], repeats_per_trial=repeat, num_trials=10, global_vars=globals())

if __name__ == '__main__':
    main()