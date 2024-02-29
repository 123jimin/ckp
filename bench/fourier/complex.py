from bench.util import bench
from ckp.fourier.complex import ComplexCooleyTukeyFFT
from ckp.fourier.util import bit_reverse_table, min_convolution_size_power

import random, cmath
random.seed(42)

X = [random.random() for _ in range(65536)]

bit_reverse_table(15)
bit_reverse_table(16)
bit_reverse_table(17)

def bench_cooley_tukey_fft():
    fft = ComplexCooleyTukeyFFT.get(16)
    fft(X)

class FFT:
    def __init__(self, N: int):
        assert N.bit_count() == 1
        self._N = N
        self._exp = [cmath.exp(2j * cmath.pi * (i / N)) for i in range(N // 2)]
        self._iexp = [c.conjugate() for c in self._exp]
        self._bit_rev = bit_reverse_table(N.bit_length() - 1)
        assert len(self._bit_rev) == N

    def __len__(self):
        return self._N

    def fft(self, A, B=None, *, inverse: bool=False):
        (N, bit_rev) = (self._N, self._bit_rev)
        exp_table = self._iexp if inverse else self._exp
        assert len(A) == N
        if B is None:
            B = [A[bit_rev[i]] for i in range(N)]
        else:
            for i in range(N):
                B[i] = A[bit_rev[i]]
        assert len(B) == N
        l = 2
        while l <= N:
            (hl, step) = (l // 2, N // l)
            for i in range(0, N, l):
                k = 0
                for j in range(i, i + hl):
                    o = B[j + hl] * exp_table[k]
                    B[j + hl] = B[j] - o
                    B[j] += o
                    k += step
            l *= 2
        if inverse:
            for i in range(N):
                B[i] /= N
        return B
    
def bench_other_fft():
    fft = FFT(65536)
    fft.fft(X)

if __name__ == '__main__':
    bench([
        "bench_cooley_tukey_fft()",
        "bench_other_fft()",
    ], num_trials=8, global_vars=globals())