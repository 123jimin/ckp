from ckp.number_theory import mobius_sieve_init

N = 2_000_000

def bench():
    Ns = N - 1
    sieve = mobius_sieve_init(Ns)
    mu = sieve.mu

    M = [m := 0]
    for k in range(1, Ns+1, 2):
        m0 = m = m + mu[k//2]
        if (k1 := k+1) & 2: m -= mu[k1//4]
        M += (m0, m)
    
    ans, i = 0, 1
    while i <= N:
        j = N // i; k = N // j
        ans += (M[k] - M[i-1]) * j * j
        i = k+1
    
    assert(ans == 2431709398555)

tags = {'mobius_inversion'}