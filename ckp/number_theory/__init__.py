from math import isqrt

def is_prime_naive(n:int) -> bool:
    """
        Naive primality testing.
        - Time: `O(sqrt(n))`
    """
    if n < 100: return n in {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}
    if n%2 == 0 or n%3 == 0 or n%5 == 0 or n%7 == 0 or n%11 == 0: return False

    for p in range(13, isqrt(n)+1, 6):
        if n%p == 0 or n%(p+4) == 0: return False
    
    return True