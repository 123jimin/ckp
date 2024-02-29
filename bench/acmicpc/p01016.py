from bench import bench as do_bench
from ckp.number_theory import PrimeSieve

def bench():
    sieve = PrimeSieve(1_000_000)
    A = 1_000_000_000_000
    B = A + 1_000_000
    is_squarefree = [True] * (B-A+1)

    for p in sieve.primes():
        ps = p*p
        pA = A
        if pA%ps > 0: pA += ps - (pA%ps)
        for q in range(pA, B+1, ps):
            is_squarefree[q-A] = False
    
    ans = sum(is_squarefree)
    assert ans == 607940
    return ans

tags = {'number_theory', 'primality_test', 'prime_sieve'}