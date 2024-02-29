import abc

class AbstractDFT(abc.ABC):
    __slots__ = ('_n',)
    _n: int

    def __init__(self, n:int): self._n = n
    def __len__(self): return self._n

    @abc.abstractmethod
    def __call__(self, in_buffer, out_buffer=None, *, inverse:bool=False):
        pass

class AbstractComplexDFT(AbstractDFT):
    @abc.abstractmethod
    def __call__(self, in_buffer:list[float|complex], out_buffer:list[float|complex]|None=None, *, inverse:bool=False):
        pass