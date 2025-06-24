from bench.util import bench
from ckp.fourier.util import bit_reverse_table

import functools, itertools, operator

@functools.cache
def bit_reverse_table_alt(L:int) -> list[int]:
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

def bench_bit_reverse_table():
    bit_reverse_table.cache_clear()
    bit_reverse_table(22)

def bench_bit_reverse_table_alt():
    bit_reverse_table_alt.cache_clear()
    bit_reverse_table_alt(22)

if __name__ == '__main__':
    bench([
        bench_bit_reverse_table,
        bench_bit_reverse_table_alt,
    ], num_trials=10)