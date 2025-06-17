import abc

class AbstractSegmentTree(abc.ABC):
    __slots__ = ('_len',)

    _len: int
    """ Amount of elements in this segment tree. """

    def __len__(self): return self._len
    def __str__(self): return "[{}]".format(", ".join(map(str, self.__iter__())))
    def __iter__(self): yield from map(self.__getitem__, range(self._len))
