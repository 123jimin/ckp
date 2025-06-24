import functools

def min_convolution_size_power(a:int|list, b:int|list) -> int:
    """ Find k such that n = 2^k is minimal size of Cooley-Tukey FFT for convoluting a and b. """
    if not isinstance(a, int): a = len(a)
    if not isinstance(b, int): b = len(b)
    x = a + b - 2
    return x.bit_length() if x > 0 else 0

@functools.cache
def bit_reverse_table(L:int) -> list[int]:
    """ Returns an array A such that it contains A[x] = (bit reversal of x) for every L-bit integers x. """
    if L < 4: return ([0], [0,1], [0,2,1,3], [0,4,2,6,1,5,3,7])[L]

    LO_BITS = L//2
    HI_BITS = L-LO_BITS
    LO_MUL, HI_MUL = 1<<LO_BITS, 1<<HI_BITS

    table_lo = [x*HI_MUL for x in bit_reverse_table(LO_BITS)]
    table_hi = bit_reverse_table(HI_BITS)

    ret = table_lo * HI_MUL
    for i in range(HI_MUL):
        v = table_hi[i]
        ii = i * LO_MUL
        for j in range(ii, ii + LO_MUL): ret[j] += v
    
    return ret