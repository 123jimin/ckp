from bench.util import bench
from ckp.fourier.util import bit_reverse_table

def bench_bit_reverse_table():
    bit_reverse_table.cache_clear()
    bit_reverse_table(21)

if __name__ == '__main__':
    bench([
        "bench_bit_reverse_table()",
    ], num_trials=8, global_vars=globals())