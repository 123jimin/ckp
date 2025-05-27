"""
    This module contains functions for computing functions related to combinatorics.
"""

from math import log, comb, lgamma, log1p
from .const import euler_gamma

def log_falling_factorial(n: int, k: int) -> float:
    """
        Computes the log value of n*(n-1)*...*(n-k+1) = n!/(n-k)! (also known as nPk), where 0 <= k <= n.
        This function is more accurate than `math.lgamma(n+1) - math.lgamma(n-k+1)`, when k is small compared to n.
    """
    assert(0 <= k <= n)

    # Degenerate case
    if n == 0: return 0

    # Exact for small values / when using lgamma once is sufficient
    if k == 0: return 0
    if k == n: return lgamma(n+1)
    if k <= 30: return sum(log(n-i) for i in range(k))

    # Computes log(n!) - log((n-k)!) using the log-gamma function.
    np1, nmkp1 = n+1, n-k+1
    log_n_fac, log_nk_fac = lgamma(np1), lgamma(nmkp1)
    log_ff_using_lgamma = log_n_fac - log_nk_fac
    
    # Check whether the result didn't suffer from rounding error.
    if log_ff_using_lgamma / log_n_fac > 1e-3: return log_ff_using_lgamma

    # Use the Stirling's approximation to compute lgamma(n+1) - lgamma(n-k+1) more accurately.
    log_diff = log1p(k/nmkp1)
    stirling_major_diff = k * (log1p(n) - 1) + (n - k + 0.5) * log_diff

    # major diff + minor_diff
    return stirling_major_diff - k / (12 * np1 * nmkp1)

def log_comb(n: int, k: int) -> float:
    """ Computes `math.log(math.comb(n, k))`, accurately for large n and/or k. Assumes that `math.comb(n, k) > 0`. """
    assert(0 <= k <= n)

    # Degenerate case
    if n == 0: return 0

    # Exact for small values
    if k == 0 or k == n: return 0
    if n <= 30: return log(comb(n, k))

    if k+k > n: k = n-k
    if k <= 30: return sum(log(n-i) - log(i+1) for i in range(k))

    # Compute log(n!) - log((n-k)!) - log(k!) using the log-gamma function.
    np1, nmkp1 = n+1, n-k+1
    log_n_fac, log_nk_fac, log_k_fac = lgamma(np1), lgamma(nmkp1), lgamma(k+1)
    log_comb_using_lgamma = log_n_fac - (log_nk_fac + log_k_fac)

    # Check whether the result didn't suffer from rounding error.
    if log_comb_using_lgamma / log_n_fac > 1e-3: return log_comb_using_lgamma

    # Use the Stirling's approximation to compute lgamma(n+1) - lgamma(n-k+1) more accurately.
    log_diff = log1p(k/nmkp1)
    stirling_major_diff = k * (log1p(n) - 1) + (n - k + 0.5) * log_diff

    # major diff + minor_diff - log_k_fac
    return stirling_major_diff - (log_k_fac + k / (12 * np1 * nmkp1))

def harmonic_number(n: int, *, _cache: list[int] = [0, 1, 1.5]) -> float:
    """ Computes H(n) = `sum(1/i for i in range(1, n+1))`, accurately for large n. """
    if n <= 0: return 0
    if n == 1: return 1
    if n < len(_cache): return _cache[n]
    if n <= 100:
        s = _cache[-1]
        for i in range(len(_cache), n+1):
            s += 1/i
            _cache.append(s)
        return s
    
    nsq = n*n
    nqd = nsq*nsq

    # Absolute error should be less than 1/n^10
    return log(n) + euler_gamma() + 1/(2*n) - 1/(12*nsq) + 1/(120*nqd) - 1/(252*nsq*nqd) + 1/(240*nqd*nqd)

def coupon_collector_expected(n: int, k: int) -> float:
    """ Computes `n*(H(n) - H(n-k))`, the expected number of coupons collected for collecting `k` of `n` coupons. """
    if k == 0: return 0
    if n == k: return n * harmonic_number(n)
    if k <= 100: return n * sum(1/(n-i) for i in range(k))
    if n-k <= 100: return n * (harmonic_number(n) - harmonic_number(n-k))
    
    r = n-k
    nn, nd = 60*n**3 - 10*n**2 + 1, 120*n**4
    rn, rd = 60*r**3 - 10*r**2 + 1, 120*r**4
    rem = ((nn*rd-nd*rn)*n)/(nd*rd)
    return rem + n*log1p(k/r)