from bench.util import bench
from ckp.fourier.complex import ComplexCooleyTukeyFFT
from ckp.fourier.util import bit_reverse_table, min_convolution_size_power

import random, cmath
random.seed(42)

X = [random.random() for _ in range(262144)]
Y = [0] * len(X)

ComplexCooleyTukeyFFT.get(18)

def bench_cooley_tukey():
    fft = ComplexCooleyTukeyFFT.get(18)
    fft(X)

if __name__ == '__main__':
    bench([
        "bench_cooley_tukey()",
    ], num_trials=8, global_vars=globals())