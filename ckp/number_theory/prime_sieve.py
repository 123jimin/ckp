from math import isqrt

class PrimeSieve:
    """
        An implementation of the sieve of Eratosthenes.
    """

    __slots__ = ('sieve', '_odd_primes', '_odd_primes_next', '_max_testable_odd')
    sieve: list[int]
    """ `sieve[k]` contains a prime factor that divides `2k+1`, or 1 if it's already a prime number. """

    _odd_primes: list[int]
    _odd_primes_next: int
    _max_testable_odd: int

    def __init__(self, max_n: int = 1):
        self.sieve = [1, 1]
        self._odd_primes = [3]
        self._odd_primes_next = 5
        self._max_testable_odd = 3

        if max_n > 1: self.extend(max_n)
    
    def primes(self):
        """ Yields list of prime numbers from this sieve. """
        yield 2
        odd_primes = self._odd_primes
        for p in odd_primes: yield p
        odd_primes_next, sieve = self._odd_primes_next, self.sieve
        for p in range(odd_primes_next, self._max_testable_odd+2, 2):
            if sieve[p//2] > 1: continue
            odd_primes.append(p)
            odd_primes_next = p+2
            yield p
        self._odd_primes_next = odd_primes_next

    def extend(self, max_n:int):
        """ Extend this sieve, so that the primality test up to `max_n` with this sieve becomes possible. """
        if max_n <= self._max_testable_odd+1: return

        sieve, odd_primes, max_testable_odd = self.sieve, self._odd_primes, self._max_testable_odd

        old_len = len(sieve)
        new_len = (max_n+1) // 2
        new_max_testable_odd = new_len*2 - 1

        sieve += [1] * (new_len - old_len)
        
        for p in odd_primes:
            min_p = p*p
            if min_p <= max_testable_odd:
                min_p = max_testable_odd + 2
                if min_p % p > 0: min_p += p - (min_p % p)
                if min_p % 2 == 0: min_p += p
            while min_p <= new_max_testable_odd:
                sieve[min_p//2] = p
                min_p += 2*p

        p = self._odd_primes_next
        p_max = isqrt(new_max_testable_odd)
        while p <= p_max: # The reason is uncertain, but using `for p in range(...)` makes the code a little bit slower.
            if sieve[p//2] == 1:
                odd_primes.append(p)
                for q in range(p*p, new_max_testable_odd+2, 2*p): sieve[q//2] = p
            p += 2
        
        self._odd_primes_next = p
        self._max_testable_odd = new_max_testable_odd
    
    def is_prime(self, n:int) -> bool:
        """
            Check whether `n` is a prime number.
            When `n` is an odd number, the sieve might get extended.
        """
        if n < 100: return n in {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}
        if n%2 == 0: return False
        if n > self._max_testable_odd: self.extend(n)
        return self.sieve[n//2] == 1
    
    def factor(self, n:int):
        """ Yields every prime factors of `n`, in no particular order. """
        if n < 2: return
        if n < 4:
            yield n
            return
        while n%2 == 0:
            n //= 2
            yield 2
        sieve = self.sieve
        if n > self._max_testable_odd: self.extend(n)
        p = sieve[n//2]
        while p > 1:
            yield p
            n //= p
            p = sieve[n//2]
        if n > 1: yield n