from ..abc import AbstractSegmentTree

class NumberSegmentTree(AbstractSegmentTree):
    """ A segment tree on integers/floats supporting range add/sum operations. """

    __slots__ = ('_tree', '_lazy')

    _tree: list
    """ A flat representation of this segment tree. """

    _lazy: list
    """ A flat representation of lazy-updates in this segment tree. """

    def __init__(self):
        raise NotImplementedError("Not yet implemented!")