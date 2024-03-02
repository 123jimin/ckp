import cmath, functools

from .abc import AbstractComplexDFT
from .util import bit_reverse_table, min_convolution_size_power

class ComplexNaiveDFT(AbstractComplexDFT):
    """ Naive discrete fourier transformation algorithm. """
    def __init__(self, n:int): super().__init__(n)

    def __str__(self) -> str: return f"ComplexNaiveDFT({len(self)})"
    def __repr__(self) -> str: return f"ComplexNaiveDFT({len(self)})"

    def __call__(self, in_buffer:list[complex], out_buffer:list[complex]|None=None, *, inverse:bool = False) -> list[complex]:
        N = len(self)
        Ns = min(N, len(in_buffer))

        if out_buffer is None: out_buffer = [0] * N
        else: assert(len(out_buffer) >= N)
        
        match N:
            case 0:
                return out_buffer
            case 1:
                out_buffer[0] = in_buffer[0] if Ns else 0
                return out_buffer

        exp = cmath.exp
        
        if inverse:
            mult = 2j*cmath.pi / N

            for k in range(N):
                k_mult = mult * k
                out_buffer[k] = sum(in_buffer[n] * exp(k_mult * n) for n in range(Ns)) / N
        else:
            mult = -2j*cmath.pi / N

            for k in range(N):
                k_mult = mult * k
                out_buffer[k] = sum(in_buffer[n] * exp(k_mult * n) for n in range(Ns))

        return out_buffer

class ComplexCooleyTukeyFFT(AbstractComplexDFT):
    """ Cooley-Tukey FFT on complex numbers, where N = 2^L. """
    __slots__ = ('_bit_rev', '_exp', '_iexp')
    _bit_rev: list[int]
    _exp: list[complex]
    _iexp: list[complex]

    def __init__(self, L:int):
        super().__init__(1<<L)
        N = len(self)

        self._bit_rev = bit_reverse_table(L)
        assert(len(self._bit_rev) == N)

        omega = -2j * cmath.pi / N
        self._exp = [cmath.exp(omega * i) for i in range(N//2)]
        self._iexp = [c.conjugate() for c in self._exp]
    
    def __str__(self) -> str: return f"ComplexCooleyTukeyFFT({len(self).bit_length() - 1})"
    def __repr__(self) -> str: return f"ComplexCooleyTukeyFFT({len(self).bit_length() - 1})"
    
    def __call__(self, data:list[float|complex], *, inverse:bool=False):
        N, bit_rev = len(self), self._bit_rev
        exp_table = self._iexp if inverse else self._exp
        
        len_data = len(data)
        if len_data == N: out_buffer = [data[i] for i in bit_rev]
        else: out_buffer = [(data[i] if i < len_data else 0) for i in bit_rev]

        if N == 1: return out_buffer

        for i in range(0, N, 2):
            ih = i+1
            oi = out_buffer[i]
            out_buffer[ih] = oi - (o := out_buffer[ih])
            out_buffer[i] = oi + o

        l = 4
        while l <= N:
            hl, step = l//2, N//l
            for i in range(0, N, l):
                k, iu = 0, i+hl
                while i < iu:
                    ih = i+hl
                    oi = out_buffer[i]
                    out_buffer[ih] = oi - (o := out_buffer[ih] * exp_table[k])
                    out_buffer[i] = oi + o
                    k += step
                    i += 1
            l += l
        
        if inverse:
            for i in range(N): out_buffer[i] /= N
        return out_buffer
    
    @staticmethod
    @functools.cache
    def get(L:int):
        return ComplexCooleyTukeyFFT(L)
    
    @staticmethod
    def get_common_fft(a:int|list, b:int|list) -> AbstractComplexDFT:
        l = min_convolution_size_power(a, b)
        if l == 0: return ComplexNaiveDFT(1)
        return ComplexCooleyTukeyFFT.get(l)

@functools.cache
def get_complex_dft(n:int) -> AbstractComplexDFT:
    """ Get an AbstractComplexDFT instance that performs DFT on an array with size n. """
    if n < 2: return ComplexNaiveDFT(n)
    l = n.bit_length() - 1
    if n == (1<<l): return ComplexCooleyTukeyFFT.get(l)
    raise NotImplementedError(f"DFT on {n} elements is not yet supported!")

def get_common_complex_dft(a:int|list, b:int|list) -> AbstractComplexDFT:
    return ComplexCooleyTukeyFFT.get_common_fft(a, b)