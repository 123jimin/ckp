"""
    This file is mainly focused on implementing nimber multiplications (multiplications in GF(2^2^n)).
"""

import functools

def nimber_mul(x:int, y:int) -> int:
    """ Returns the nimber product of x and y. """

    if x == 0 or y == 0: return 0
    if x == 1: return y
    if y == 1: return x

    y_b, y_odd = divmod(y, 2)
    y_bin, i = [], 1

    while y_b:
        y_b, r = divmod(y_b, 2)
        if r: y_bin.append(i)
        i += 1

    x_b, x_odd = divmod(x, 2)

    v = (y if x_odd else 0) ^ (x if y_odd else 0) ^ (x_odd and y_odd)

    i = 1
    while x_b:
        x_b, r = divmod(x_b, 2)
        if r:
            for yi in y_bin: v ^= nimber_mul_2exp(i, yi)
        i += 1
    return v

@functools.cache
def nimber_mul_2exp(x: int, y: int) -> int:
    """ Returns nimber product of 2^x and 2^y. """

    if x < y: x, y = y, x
    if y == 0: return 2**x
    
    xf, yf = x.bit_length()-1, y.bit_length()-1
    assert(xf >= yf >= 0)

    d = 2**xf
    assert(1 <= d <= x < 2*d)

    if xf != yf:
        v = (2**d) * nimber_mul_2exp(x-d, y)
    elif x == d:
        assert(y == d)
        v = 3*(2**(d-1))
    else:
        v = nimber_mul_2exp(x-d, y-d)
        v = ((2**d) * v) ^ nimber_mul(v, 2**(d-1))
    return v

class Nimber:
    """
        Class for dealing nimbers.

        Using this class, at the expense of performance, may simplify codes involving nimbers.

        Still, as the performance hit is severe, using `^` and `nimber_mul` directly is recommended.
    """

    __slots__ = ('value',)

    def __init__(self, value):
        if isinstance(value, Nimber): self.value = value.value
        else: self.value = value
    
    def __repr__(self): return f"Nimber({self.value})"
    def __str__(self): return str(self.value)
    def __bool__(self): return self.value != 0
    def __index__(self): return self.value

    def __eq__(self, other): return self.value == (other.value if isinstance(other, Nimber) else other)
    def __ne__(self, other): return self.value != (other.value if isinstance(other, Nimber) else other)

    def __add__(self, other): return Nimber(self.value ^ (other.value if isinstance(other, Nimber) else other))
    def __radd__(self, other): return Nimber(self.value ^ other)

    def __iadd__(self, other): self.value ^= (other.value if isinstance(other, Nimber) else other); return self
    
    def __sub__(self, other): return Nimber(self.value ^ (other.value if isinstance(other, Nimber) else other))
    def __rsub__(self, other): return Nimber(self.value ^ other)

    def __isub__(self, other): self.value ^= (other.value if isinstance(other, Nimber) else other); return self

    def __mul__(self, other): return Nimber(nimber_mul(self.value, (other.value if isinstance(other, Nimber) else other)))
    def __rmul__(self, other): return Nimber(nimber_mul(self.value, other))