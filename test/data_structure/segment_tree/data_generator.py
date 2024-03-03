import random

class DataGenerator:
    __slots__ = ('N', 'ops')

    def __init__(self, N, ops=None):
        self.N = N
        self.ops = ops

    def index(self) -> int:
        return random.randrange(0, self.N)

    def range(self) -> tuple[int, int]:
        i = random.randrange(0, self.N)
        j = random.randrange(i, self.N+1)

        return (i, j)
    
    def value(self) -> int:
        return random.randint(-100, 100)
    
    def list(self) -> list[int]:
        return [self.value() for _ in range(self.N)]

    def op(self):
        match random.choice(self.ops):
            case 'add_to': return ('add_to', *self.range(), self.value())
            case 'get': return ('get', self.index())
            case 'set': return ('set', self.index(), self.value())
            case 'reduce': return ('reduce', *self.range())
            case 'reduce_all': return ('reduce_all',)