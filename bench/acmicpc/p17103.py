from ckp.number_theory import prime_sieve_init, prime_sieve_primes, prime_sieve_query

import random
V = [random.randint(450_000, 500_000)*2 for _ in range(100)]

def bench():
    sieve = prime_sieve_init(1_000_000)
    primes = {p: 1 for p in prime_sieve_primes(sieve)}

    ans = 0
    for v in V:
        v2 = v // 2
        for p in primes:
            if p > v2: break
            ans += (v-p) in primes
    assert(ans == 578977)

tags = {'number_theory', 'primality_test', 'prime_sieve'}