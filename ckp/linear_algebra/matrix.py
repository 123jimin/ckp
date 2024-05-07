"""
    Codes for performing matrix operations on an arbitrary ring.
    For performing matrix operations on Z/nZ, using `ckp.linear_algebra.matrix_mod` is recommended.
"""

def column_vec(x: list) -> list[list]: return [[xe] for xe in x]

def matrix_id(n: int):
    """ Returns an n-by-n identity matrix, where 0 is the additive identity and 1 is the multiplicative identity. """
    return [[int(i == j) for j in range(n)] for i in range(n)]

def matrix_copy(x: list[list]):
    return [row.copy() for row in x]

def matrix_add(x: list[list], y: list[list]) -> list[list]:
    return [[xe+ye for (xe, ye) in zip(xr, yr)] for (xr, yr) in zip(x, y)]

def matrix_iadd(x: list[list], y: list[list]) -> list[list]:
    for (xr, yr) in zip(x, y):
        for i in range(len(xr)): xr[i] += yr[i]
    return x

def matrix_sub(x: list[list], y: list[list]) -> list[list]:
    return [[xe-ye for (xe, ye) in zip(xr, yr)] for (xr, yr) in zip(x, y)]

def matrix_isub(x: list[list], y: list[list]) -> list[list]:
    for (xr, yr) in zip(x, y):
        for i in range(len(xr)): xr[i] -= yr[i]
    return x

def matrix_neg(x: list[list]) -> list[list]:
    return [[-xe for xe in xr] for xr in x]

def matrix_mul(x: list[list], y: list[list]) -> list[list]:
    assert(0 < len(x[0]) == len(y))

    I, J, K = len(x), len(y), len(y[0])

    return [[sum(x[i][j]*y[j][k] for j in range(J)) for k in range(K)] for i in range(I)]

def matrix_scalar_mul(x: list[list], k) -> list[list]:
    return [[k*xe for xe in xr] for xr in x]

def matrix_scalar_imul(x: list[list], k) -> list[list]:
    for xr in x:
        for i in range(len(xr)): xr[i] *= k
    return x

def matrix_column_mul(a: list[list], v: list) -> list:
    """ Computes Av, for a matrix and a column vector. """
    return [sum(aij*vj for (aij, vj) in zip(ai, v)) for ai in a]

def matrix_pow(x: list[list], k: int) -> list[list]:
    assert(0 <= len(x) == len(x[0]))
    assert(k >= 0)

    if k == 0: return matrix_id(len(x))
    if k == 1: return matrix_copy(x)

    k, d = divmod(k, 2)
    y = matrix_pow(x, k)
    y = matrix_mul(y, y)

    if d: y = matrix_mul(y, x)
    return y

def matrix_equal(x: list[list], y: list[list]) -> bool:
    if len(x) != len(y): return False
    return all(len(xr) == len(yr) and all(xe == ye for (xe, ye) in zip(xr, yr)) for (xr, yr) in zip(x, y))

class Matrix:
    """ A generic matrix class. """
    __slots__ = ('rows')
    def __init__(self, rows: list[list]):
        self.rows = rows
    
    def __repr__(self): return f"Matrix({repr(self.rows)})"
    def __str__(self): return f"Matrix({str(self.rows)})"

    def __len__(self) -> int: return len(self.rows)
    def size(self) -> tuple[int, int]: return (len(self.rows), len(self.rows[0])) if len(self.rows) else (0, 0)

    def copy(self): return Matrix(matrix_copy(self.rows))

    def __call__(self, v: list) -> list:
        return matrix_column_mul(self.rows, v)

    def __eq__(self, other):
        if isinstance(other, Matrix): return matrix_equal(self.rows, other.rows)
        elif isinstance(other, (list, tuple)): return matrix_equal(self.rows, other)
        else: return NotImplemented
    
    def __ne__(self, other): return not self.__eq__(other)
    
    def __add__(self, other):
        if isinstance(other, Matrix): return Matrix(matrix_add(self.rows, other.rows))
        elif isinstance(other, (list, tuple)): return Matrix(matrix_add(self.rows, other))
        else: return NotImplemented
        
    def __iadd__(self, other):
        if isinstance(other, Matrix): matrix_iadd(self.rows, other.rows)
        elif isinstance(other, (list, tuple)): matrix_iadd(self.rows, other)
        else: return NotImplemented
        return self
    
    def __radd__(self, other):
        if isinstance(other, (list, tuple)): return Matrix(matrix_add(other, self.rows))
        else: return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, Matrix): return Matrix(matrix_sub(self.rows, other.rows))
        elif isinstance(other, (list, tuple)): return Matrix(matrix_sub(self.rows, other))
        else: return NotImplemented
        
    def __isub__(self, other):
        if isinstance(other, Matrix): matrix_isub(self.rows, other.rows)
        elif isinstance(other, (list, tuple)): matrix_isub(self.rows, other)
        else: return NotImplemented
        return self
    
    def __rsub__(self, other):
        if isinstance(other, (list, tuple)): return Matrix(matrix_sub(other, self.rows))
        else: return NotImplemented
    
    def __neg__(self):
        return Matrix(matrix_neg(self.rows))
    
    def __mul__(self, other):
        if isinstance(other, Matrix): return Matrix(matrix_mul(self.rows, other.rows))
        elif isinstance(other, (list, tuple)): return Matrix(matrix_mul(self.rows, other))
        else: return Matrix(matrix_scalar_mul(self.rows, other))
    
    def __imul__(self, other):
        if isinstance(other, Matrix): self.rows = matrix_mul(self.rows, other.rows)
        elif isinstance(other, (list, tuple)): self.rows = matrix_mul(self.rows, other)
        else: matrix_scalar_imul(self.rows, other)
        return self
    
    def __rmul__(self, other):
        if isinstance(other, (list, tuple)): return Matrix(matrix_sub(other, self.rows))
        else: return Matrix(matrix_scalar_mul(self.rows, other))
    
    def __pow__(self, other):
        if isinstance(other, int): return Matrix(matrix_pow(self.rows, other))
        else: return NotImplemented