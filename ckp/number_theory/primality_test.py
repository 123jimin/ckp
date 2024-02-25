from math import isqrt

def is_prime_naive(n: int) -> bool:
    """
        Naive primality testing.
        - Time: `O(sqrt(n))`
    """
    if n < 100: return n in {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}
    if n%2 == 0 or n%3 == 0 or n%5 == 0 or n%7 == 0 or n%11 == 0: return False

    for p in range(13, isqrt(n)+1, 6):
        if n%p == 0 or n%(p+4) == 0: return False
    
    return True

def is_prime_miller_rabin(n: int) -> bool:
    """
        Primality testing using Miller-Rabin.
        - Time: `O(log^4(n))`
    """
    if n < 2: return False
    if n < 4 or n == 5 or n == 7: return True
    if n%2 == 0 or n%3 == 0 or n%5 == 0 or n%7 == 0: return False
    if n < 121: return True

    d = n-1
    r = (d & -d).bit_length()-1
    d >>= r

    al = ()
    
    if n < 2047: al = (2,)
    elif n < 9080191: al = (31, 73)
    elif n < 4759123141: al = (2, 7, 61)
    elif n < 2152302898747: al = (2, 3, 5, 7, 11)
    elif n < 3474749660383: al = (2, 3, 5, 7, 11, 13)
    elif n < 341550071728321: al = (2, 3, 5, 7, 11, 13, 17)
    elif n < 3825123056546413051: al = (2, 3, 5, 7, 11, 13, 17, 19, 23)
    elif n < 318665857834031151167461: al = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    elif n < 3317044064679887385961981: al = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    else: al = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)

    for a in al:
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        comp = True
        for _ in range(r-1):
            x *= x
            x %= n
            if x == n-1:
                comp = False
                break
        if comp: return False
    return True

def is_prime(n: int) -> bool:
    """
        Returns whether `n` is a prime number. The best algorithm will be picked depending on `n`.
    """
    return (is_prime_naive if n <= 160_000 else is_prime_miller_rabin)(n)