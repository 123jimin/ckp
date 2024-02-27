import cmath

class ComplexNaiveDFT:
    """ Naive discrete fourier transformation algorithm. """

    __slots__ = ('_n',)
    _n: int

    def __init__(self, n:int): self._n = n
    def __len__(self): return self._n

    def __str__(self) -> str: return f"ComplexNaiveDFT({len(self)})"
    def __repr__(self) -> str: return f"ComplexNaiveDFT({len(self)})"

    def __call__(self, in_buffer:list[complex], out_buffer:list[complex]|None=None, *, inverse:bool = False) -> list[complex]:
        N = len(self)
        Ns = min(N, len(in_buffer))
        if out_buffer is None: out_buffer = [0] * N
        if inverse:
            mult = 2*cmath.pi / N

            for k in range(N):
                k_mult = mult * k
                out_buffer[k] = sum(in_buffer[n] * cmath.exp(complex(0, k_mult * n)) for n in range(Ns)) / N
        else:
            mult = -2*cmath.pi / N

            for k in range(N):
                k_mult = mult * k
                out_buffer[k] = sum(in_buffer[n] * cmath.exp(complex(0, k_mult * n)) for n in range(Ns))

        return out_buffer
