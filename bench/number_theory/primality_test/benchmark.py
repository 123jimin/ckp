from bench.util import bench
from ckp.number_theory.primality_test import is_prime_miller_rabin_with_base

def is_prime_miller_rabin_with_base_alt(n: int, al: list[int]) -> bool:
    d = n1 = n-1
    r = (d & -d).bit_length()-1
    d >>= r

    for a in al:
        x = pow(a, d, n)
        if x == 1 or x == n1: continue
        for _ in range(r-1):
            if (x := (x*x)%n) == n1: break
            elif x == 1: return False
        else:
            return False
    
    return True

x = 0

def main():
    global x

    TEST_DATA: list[tuple[int, int, int]] = [
        (4,  7,  200_000),
        (6,  3,  200_000),
        (8,  7,  200_000),
        (9,  7,  200_000),
        (20, 39, 200_000),
        # (50, 151, 100),
        # (200, 357, 10),
    ]

    for (k, d, repeat) in TEST_DATA:
        x = 10**k + d
        print(f"Testing: 10**{k}+{d} ({repeat} times)")
        bench([
            "is_prime_miller_rabin_with_base    (x, (31, 73))",
            "is_prime_miller_rabin_with_base_alt(x, (31, 73))",
        ], repeats_per_trial=repeat, num_trials=10, global_vars=globals())

if __name__ == '__main__':
    main()