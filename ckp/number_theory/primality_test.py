from math import isqrt

def is_prime_trial_division(n: int) -> bool:
    """ Primality testing using trial division. Slow but good enough for simple problems. """
    if n < 53: return n in {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}
    if not((n&1) and n%3 and n%5 and n%7 and n%11 and n%13): return False
    if n < 289: return True
    for p in range(17, isqrt(n)+1, 6):
        if not(n%p and n%(p+2)): return False
    return True

def is_prime_trial_division_fast(n: int) -> bool:
    """
        Primality test using trial division. Consider using `is_prime_trial_division` or `is_prime` instead of this one.
        - Time: `O(sqrt(n))`
    """

    # Fast path for small `n`.
    if n < 151: return n in {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
    }

    # Weed out composite numbers with small factors.
    if not((n&1) and n%3 and n%5 and n%7 and n%11 and n%13 and n%17 and n%19): return False
    if n < 1591: return n not in {
        529, 667, 713, 841, 851, 899, 943, 961, 989, 1073, 1081, 1147, 1189, 1219,
        1247, 1271, 1333, 1357, 1363, 1369, 1403, 1457, 1517, 1537, 1541,
    }
    
    # Trial division with period of 30.
    # Note: Using `all(...)` is tempting, but it's actually slower.
    for p in range(23, isqrt(n)+1, 30):
        if n%p and n%(p+6) and n%(p+8) and n%(p+14) and n%(p+18) and n%(p+20) and n%(p+24) and n%(p+26): continue
        return False
    
    return True

def is_prime_miller_rabin_with_base(n: int, al: list[int]) -> bool:
    """ Returns whether `n` is a probable prime, using `al` as a list of bases for the Miller-Rabin test. """
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

def is_prime(n: int) -> bool:
    """
        Returns whether `n` is a prime number, with a combination of following methods:
        - Small lookup table of prime numbers.
        - Trial division with small factors.
        - Fermat primality test with lookup table of false positives.
        - Miller-Rabin with shortest possible bases.
    """

    # Fast path for small `n`.
    if n < 127: return n in {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
        67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
    }

    if not(n&1): return False

    if n <= 3828001 and n in {
        # Small composite numbers with large prime factors.
        1369, 1517, 1591, 1681, 1739, 1763, 1849, 1927, 1961, 2021, 2173,
        2183, 2209, 2257, 2279, 2419, 2479, 2491, 2501, 2537, 2623, 2627,
        # Small Fermat pseudoprimes with base=45.
        3053, 6533, 8321, 21667, 37969, 42127, 43553, 96049, 104441, 112141, 118301,
        130561, 146611, 157693, 188501, 191351, 220669, 252601, 262393, 270481, 275887,
        # Small Fermat pseudoprimes with base=45 and 158.
        470017, 485357, 1357441, 1904033, 2538251, 3057601, 3647621, 3818413, 3822607, 3828001,
    }: return False

    # Weed out composite numbers with small factors.
    if not(n%3 and n%5 and n%7 and n%11 and n%13): return False
    if n < 2701: return not not(n%17 and n%19 and n%23 and n%29 and n%31)

    # Fermat test using base=45 and 158.
    if n < 4209661:
        if not(n%17 and n%19 and n%23 and n%29 and n%31 and n%37): return False
        allowed = (1, n-1)
        nh = n >> 1

        if pow(45, nh, n) not in allowed: return False
        if n < 310381: return True
        
        if pow(158, nh, n) not in allowed: return False
        return True
    
    # For brevity. At this point, overhead caused by this is ignorable.
    p23 = (2, 3, 5, 7, 11, 13, 17, 19, 23)
    return is_prime_miller_rabin_with_base(n,
        (31, 73) if n < 9080191 else 
        (2, 7, 61) if n < 4759123141 else 
        (2, 3, 5, 7, 11) if n < 2152302898747 else 
        (2, 3, 5, 7, 11, 13) if n < 3474749660383 else 
        (2, 3, 5, 7, 11, 13, 17) if n < 341550071728321 else 
        p23 if n < 3825123056546413051 else 
        (*p23, 29, 31, 37) if n < 318665857834031151167461 else 
        (*p23, 29, 31, 37, 41) if n < 3317044064679887385961981 else 
        (*p23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
    )