import math

def is_prime_naive(n: int) -> bool:
    """
        Naive primality testing.
        - Time: `O(sqrt(n))`
    """
    if n < 100: return n in {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}
    if not(n%2 and n%3 and n%5 and n%7 and n%11): return False
    
    for p in range(13, math.isqrt(n)+1, 6):
        if not(n%p and n%(p+4)): return False
    
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
    """ Returns whether `n` is a prime number. The best algorithm will be picked depending on `n`. """
    if n < 100: return n in {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}
    if not(n%2 and n%3 and n%5 and n%7 and n%11): return False
    
    if n <= 90_000:
        for p in range(13, math.isqrt(n)+1, 6):
            if not(n%p and n%(p+4)): return False
        
        return True
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