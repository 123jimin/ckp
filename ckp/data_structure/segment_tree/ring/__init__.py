class NumberRingSegmentTree:
    """ Temporary implementation for RingSegmentTree. """

    def __init__():
        raise NotImplementedError("Not yet implemented!")
    
    def __len__(self):
        raise NotImplementedError("Not yet implemented!")
    
    def __str__(self): return "[{}]".format(", ".join(map(str, self.__iter__())))
    def __iter__(self):
        for i in range(self._len): yield self.__getitem__(i)
    
    def __getitem__(self, ind: int):
        return self.sum_range(ind, ind + 1)

    def sum_range(self, start: int, end: int):
        raise NotImplementedError("Not yet implemented!")
    
    def sum_all(self):
        return self.sum_range(0, len(self))

    def __setitem__(self, ind: int, value):
        self.mul_add_to_range(ind, ind + 1, 0, value)

    def set_range(self, start: int, end: int, value):
        self.mul_add_to_range(start, end, 0, value)

    def add_to(self, ind: int, value):
        self.mul_add_to_range(ind, ind + 1, 1, value)

    def add_to_range(self, start: int, end: int, value):
        self.mul_add_to_range(start, end, 1, value)
    
    def mul_to(self, ind: int, value):
        self.mul_add_to_range(ind, ind + 1, value, 0)

    def mul_to_range(self, start: int, end: int, value):
        self.mul_add_to_range(start, end, value, 0)

    def mul_add_to(self, ind: int, m, d):
        self.mul_add_to_range(ind, ind + 1, m, d)
    
    def mul_add_to_range(self, start: int, end: int, m, d):
        raise NotImplementedError("Not yet implemented!")