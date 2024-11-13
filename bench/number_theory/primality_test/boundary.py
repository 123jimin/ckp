"""
    Determine what is a good bound to switch between different primality tests.
"""

from bench.util import bench
from ckp.number_theory.primality_test import is_prime, is_prime_naive, is_prime_miller_rabin_with_base

def is_prime_miller_rabin(n: int) -> bool:
    if n < 100: return n in {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}
    if not(n%2 and n%3 and n%5 and n%7 and n%11): return False

    return is_prime_miller_rabin_with_base(n,
        (31, 73) if n < 9080191 else 
        (2, 7, 61) if n < 4759123141 else 
        (2, 3, 5, 7, 11) if n < 2152302898747 else 
        (2, 3, 5, 7, 11, 13) if n < 3474749660383 else 
        (2, 3, 5, 7, 11, 13, 17) if n < 341550071728321 else 
        (2, 3, 5, 7, 11, 13, 17, 19, 23) if n < 3825123056546413051 else 
        (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37) if n < 318665857834031151167461 else 
        (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41) if n < 3317044064679887385961981 else 
        (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
    )

def bench_range(f, N: int):
    return sum(f(x) for x in range(N+(1 - N%2), N+1000, 2))

TEST_PRIME_LISTS = dict()
def init_test_prime_list(N: int):
    if N in TEST_PRIME_LISTS: return
    test_primes = []
    curr_p = N + (1 - N%2)
    while len(test_primes) < 1000:
        if is_prime(curr_p): test_primes.append(curr_p)
        curr_p += 2
    TEST_PRIME_LISTS[N] = test_primes

def bench_prime(f, N: int):
    test_primes = TEST_PRIME_LISTS[N]
    ans = sum(f(x) for x in test_primes)
    assert(ans == len(test_primes))
    return ans

def main(N: int):
    init_test_prime_list(N)

    print(f"Testing with {N=}:")
    bench([
        f"bench_range(is_prime_naive       , {N})",
        f"bench_range(is_prime_miller_rabin, {N})",
        f"bench_prime(is_prime_naive       , {N})",
        f"bench_prime(is_prime_miller_rabin, {N})",
    ], repeats_per_trial=50, num_trials=10, global_vars=globals())

if __name__ == '__main__':
    main(10_000)
    main(80_000)
    main(100_000)
    main(200_000)