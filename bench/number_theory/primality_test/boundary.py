"""
    Determine what is a good bound to switch between different primality tests.
"""

from bench.util import bench
from ckp.number_theory.primality_test import is_prime, is_prime_naive, is_prime_miller_rabin_with_base
from math import isqrt

def is_prime_with_naive(n: int) -> bool:
    # Fast path for small `n`.
    if n < 127: return n in {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
        67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
    }

    if not(n&1): return False

    if n <= 2627 and n in {
        # Small composite numbers with large prime factors.
        1369, 1517, 1591, 1681, 1739, 1763, 1849, 1927, 1961, 2021, 2173,
        2183, 2209, 2257, 2279, 2419, 2479, 2491, 2501, 2537, 2623, 2627,
        # Small Fermat pseudoprime with base=45.
    }: return False

    # Weed out composite numbers with small factors.
    if not(n%3 and n%5 and n%7 and n%11 and n%13): return False
    if n < 2701: return not not(n%17 and n%19 and n%23 and n%29 and n%31)

    if not(n%17 and n%19): return False

    # Trial division with period of 30.
    # Note: Using `all(...)` is tempting, but it's actually slower.
    for p in range(23, isqrt(n)+1, 30):
        if n%p and n%(p+6) and n%(p+8) and n%(p+14) and n%(p+18) and n%(p+20) and n%(p+24) and n%(p+26): continue
        return False
    
    return True

def is_prime_with_fermat(n: int) -> bool:
    # Fast path for small `n`.
    if n < 127: return n in {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
        67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
    }

    if not(n&1): return False

    if n <= 3057601 and n in {
        # Small composite numbers with large prime factors.
        1369, 1517, 1591, 1681, 1739, 1763, 1849, 1927, 1961, 2021, 2173,
        2183, 2209, 2257, 2279, 2419, 2479, 2491, 2501, 2537, 2623, 2627,
        # Small Fermat pseudoprimes with base=45.
        3053, 6533, 8321, 21667, 37969, 42127, 43553, 96049, 104441, 112141, 118301,
        130561, 146611, 157693, 188501, 191351, 220669, 252601, 262393, 270481, 275887,
        # Small Fermat pseudoprimes with base=45 and 158.
        470017, 485357, 1357441, 1904033, 2538251, 3057601,
    }: return False

    # Weed out composite numbers with small factors.
    if not(n%3 and n%5 and n%7 and n%11 and n%13): return False
    if n < 2701: return not not(n%17 and n%19 and n%23 and n%29 and n%31)

    if not(n%17 and n%19 and n%23 and n%29 and n%31 and n%37): return False

    allowed = (1, n-1)
    if pow(45, n>>1, n) not in allowed: return False
    if n < 310381: return True
    
    if pow(158, n>>1, n) not in allowed: return False
    if n < 3647621: return True

    return True

def is_prime_with_mr(n: int) -> bool:
    # Fast path for small `n`.
    if n < 127: return n in {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
        67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
    }

    if not(n&1): return False

    if n <= 2627 and n in {
        # Small composite numbers with large prime factors.
        1369, 1517, 1591, 1681, 1739, 1763, 1849, 1927, 1961, 2021, 2173,
        2183, 2209, 2257, 2279, 2419, 2479, 2491, 2501, 2537, 2623, 2627,
    }: return False

    # Weed out composite numbers with small factors.
    if not(n%3 and n%5 and n%7 and n%11 and n%13): return False
    if n < 2701: return not not(n%17 and n%19 and n%23 and n%29 and n%31)

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
        f"bench_range(is_prime_with_naive  , {N})",
        f"bench_range(is_prime_with_fermat , {N})",
        f"bench_range(is_prime_with_mr     , {N})",
        f"bench_prime(is_prime_with_fermat , {N})",
        f"bench_prime(is_prime_with_mr     , {N})",
    ], repeats_per_trial=50, num_trials=10, global_vars=globals())

if __name__ == '__main__':
    main(50_000)
    main(100_000)
    main(200_000)
    main(1_000_000)
    main(5_000_000)
    main(9080191)
    main(4759123141)