"""
    2D and 3D vector classes and methods for geometric applications.
"""

from dataclasses import dataclass
from math import hypot

@dataclass
class Vec2:
    x: float
    y: float
    def __bool__(self): return bool(self.x) or bool(self.y)
    def __iter__(self): yield self.x; yield self.y
    def __add__(self, other): return Vec2(self.x + other.x, self.y + other.y)
    def __sub__(self, other): return Vec2(self.x - other.x, self.y - other.y)
    def __neg__(self): return Vec2(-self.x, -self.y)
    def __mul__(self, other):
        if isinstance(other, Vec2): return self.x * other.x + self.y * other.y
        else: return Vec2(self.x * other, self.y * other)
    def __rmul__(self, other): return Vec2(other * self.x, other * self.y)
    def __div__(self, other): return Vec2(self.x / other, self.y / other)
    def norm(self): return hypot(self.x, self.y)
    def norm_sq(self): return self.x*self.x + self.y*self.y

    def orientation(self, v, w):
        """ Returns positive if `w` is located "counter-clockwise" from `v`. """
        dv = v-self; dw = w-self
        return dv.x * dw.y - dv.y * dw.x
    
@dataclass
class Vec3:
    x: float
    y: float
    z: float
    def __bool__(self): return bool(self.x) or bool(self.y) or bool(self.z)
    def __iter__(self): yield self.x; yield self.y; yield self.z
    def __add__(self, other): return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other): return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    def __neg__(self): return Vec3(-self.x, -self.y, -self.z)
    def __mul__(self, other):
        if isinstance(other, Vec3): return self.x * other.x + self.y * other.y + self.z * other.z
        else: return Vec3(self.x * other, self.y * other, self.z * other)
    def __rmul__(self, other): return Vec3(other * self.x, other * self.y, other * self.z)
    def __div__(self, other): return Vec3(self.x / other, self.y / other, self.z / other)
    def norm(self): return hypot(self.x, self.y)
    def norm_sq(self): return self.x*self.x + self.y*self.y
    def __matmul__(self, other): return Vec3(self.y * other.z - self.z * other.y, self.z * other.x - other.z * self.x, self.x * other.y - self.y * other.x)

    def norm(self): return hypot(self.x, self.y, self.z)
    def norm_sq(self): return self.x*self.x + self.y*self.y + self.z*self.z