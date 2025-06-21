from ckp.number_theory import prime_sieve_init, prime_sieve_primes, prime_sieve_query

import random
V = [random.randint(450_000, 500_000)*2 for _ in range(100)]

def bench():
    sieve = prime_sieve_init(1_000_000)
    ans = 0
    for v in V:
        v2 = v // 2
        for p in prime_sieve_primes(sieve):
            if p >= v2: break
            ans += prime_sieve_query(sieve, v-p)
    assert(ans == 578969)

tags = {'number_theory', 'primality_test', 'prime_sieve'}