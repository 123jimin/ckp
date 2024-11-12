import math, itertools

class PrimeSieveData:
    """ An implementation of the sieve of Eratosthenes. """
    __slots__ = ('_sieve', '_odd_primes', '_odd_primes_next', '_max_testable_odd')
    _sieve: list[int]
    """ `_sieve[k]` contains a prime factor that divides `2k+1`, or 1 if it's already a prime number. """

    _odd_primes: list[int]
    _odd_primes_next: int
    _max_testable_odd: int

    def __init__(self, max_n: int = 1):
        self._sieve = [1, 1]
        self._odd_primes = [3]
        self._odd_primes_next = 5
        self._max_testable_odd = 3

        if max_n > 1: prime_sieve_extend(self, max_n)

class PrimeSieve(PrimeSieveData):
    def extend(self, max_n: int): prime_sieve_extend(self, max_n)
    def is_prime(self, n: int) -> bool: return prime_sieve_query(self, n)
    def primes(self): return prime_sieve_primes(self)
    def factor(self, n: int): return prime_sieve_factor(self, n)

def prime_sieve_extend(sieve: PrimeSieveData, max_n: int):
    """ Extend the sieve, so that the primality test up to `max_n` with this sieve becomes possible. """
    if max_n <= sieve._max_testable_odd+1: return

    sieve_arr, odd_primes, max_testable_odd = sieve._sieve, sieve._odd_primes, sieve._max_testable_odd

    old_len = len(sieve_arr)
    new_len = (max_n+1) // 2
    new_max_testable_odd = new_len*2 - 1

    sieve_arr.extend(itertools.repeat(1, new_len - old_len))

    for p in odd_primes:
        sieve_p = p*p
        if sieve_p <= max_testable_odd:
            sieve_p = max_testable_odd + 2
            if sieve_p % p: sieve_p += p - (sieve_p % p)
            if sieve_p % 2 == 0: sieve_p += p
        elif sieve_p > new_max_testable_odd:
            break
        for k in range(sieve_p//2, new_len, p):
            sieve_arr[k] = p

    p_max = math.isqrt(new_max_testable_odd)

    for k in range(sieve._odd_primes_next//2, p_max//2+1):
        if sieve_arr[k] == 1:
            p = k+k+1
            odd_primes.append(p)
            for q in range((k+k)*(1+k), new_len, p): sieve_arr[q] = p
        
    sieve._odd_primes_next = max(sieve._odd_primes_next, p_max + 2)
    sieve._max_testable_odd = new_max_testable_odd

def prime_sieve_primes(sieve: PrimeSieveData):
    """ Yields list of prime numbers inferable from the sieve. """
    yield 2
    odd_primes, sieve_arr = sieve._odd_primes, sieve._sieve
    odd_primes.extend(k*2+1 for k in range(sieve._odd_primes_next//2, sieve._max_testable_odd//2+1) if sieve_arr[k] == 1)
    yield from odd_primes
    sieve._odd_primes_next = sieve._max_testable_odd + 2

def prime_sieve_query(sieve: PrimeSieveData, n: int) -> bool:
    """
        Check whether `n` is a prime number, querying `sieve`.
        When `n` is an odd number, the sieve might get extended.
    """
    if n < 100: return n in {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}
    m, d = divmod(n, 2)
    if d == 0: return False
    if n > sieve._max_testable_odd: sieve.extend(n)
    return sieve._sieve[m] == 1

def prime_sieve_factor(sieve: PrimeSieveData, n: int):
    """ Yields every prime factors of `n`, in no particular order. """
    if n < 2: return
    if n < 4:
        yield n
        return
    while n%2 == 0:
        n //= 2
        yield 2
    sieve_arr = sieve._sieve
    if n > sieve._max_testable_odd:
        prime_sieve_extend(sieve, n)
    p = sieve_arr[n//2]
    while p > 1:
        yield p
        n //= p
        p = sieve_arr[n//2]
    if n > 1: yield n