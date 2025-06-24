"""
    2D and 3D vector classes and methods for geometric applications.
    Unfortunately, usage of Vec2 and Vec3 are discouraged as the performance cost is non-negligible (2x slower than using tuples).
"""

from dataclasses import dataclass
from math import hypot

def vec2_dist_sq(v: tuple[float, float], w: tuple[float, float]) -> float:
    vx, vy = v; wx, wy = w; dx, dy = vx-wx, vy-wy
    return dx*dx + dy*dy

def vec2_orientation(o: tuple[float, float], v: tuple[float, float], w: tuple[float, float]) -> float:
    """ Returns positive if `w` is located counter-clockwise from `v`, relative to `o`. """
    ox, oy = o
    return (v[0]-ox)*(w[1]-oy) - (v[1]-oy)*(w[0]-ox)

def vec2_is_ccw(o: tuple[float, float], v: tuple[float, float], w: tuple[float, float]) -> bool:
    """ Slightly more efficient version of `vec2_orientation(o, v, w) > 0`. """
    ox, oy = o
    return (v[0]-ox)*(w[1]-oy) > (v[1]-oy)*(w[0]-ox)

@dataclass
class Vec2:
    x: float
    y: float
    def __bool__(self): return bool(self.x) or bool(self.y)
    def __iter__(self): yield self.x; yield self.y
    def __add__(self, other): return Vec2(self.x + other.x, self.y + other.y)
    def __sub__(self, other): return Vec2(self.x - other.x, self.y - other.y)
    def __neg__(self): return Vec2(-self.x, -self.y)
    def __mul__(self, other) -> float:
        if isinstance(other, Vec2): return self.x * other.x + self.y * other.y
        else: return Vec2(self.x * other, self.y * other)
    def __rmul__(self, other): return Vec2(other * self.x, other * self.y)
    def __truediv__(self, other): return Vec2(self.x / other, self.y / other)
    def norm(self) -> float: return hypot(self.x, self.y)
    def norm_sq(self) -> float: return self.x*self.x + self.y*self.y
    def dist(self, other) -> float: return hypot(self.x-other.x, self.y-other.y)
    def dist_sq(self, other) -> float: dx, dy = self.x-other.x, self.y-other.y; return dx*dx + dy*dy

    def orientation(self, v, w):
        """ Returns positive if `w` is located counter-clockwise from `v`. """
        dv = v-self; dw = w-self
        return dv.x * dw.y - dv.y * dw.x

def vec3_add(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def vec3_sub(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def vec3_scalar_mul(a: tuple[float, float, float], k: float) -> tuple[float, float, float]:
    return (a[0]*k, a[1]*k, a[2]*k)

def vec3_dot(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def vec3_cross(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
    ax, ay, az = a; bx, by, bz = b; return (ay*bz - az*by, az*bx - ax*bz, ax*by - ay*bx)

def vec3_dist(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return hypot(a[0]-b[0], a[1]-b[1], a[2]-b[2])

def vec3_dist_sq(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    dx, dy, dz = a[0]-b[0], a[1]-b[1], a[2]-b[2]; return dx*dx + dy*dy + dz*dz

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
    def __mul__(self, other) -> float:
        if isinstance(other, Vec3): return self.x * other.x + self.y * other.y + self.z * other.z
        else: return Vec3(self.x * other, self.y * other, self.z * other)
    def __rmul__(self, other): return Vec3(other * self.x, other * self.y, other * self.z)
    def __truediv__(self, other): return Vec3(self.x / other, self.y / other, self.z / other)
    def __matmul__(self, other): return Vec3(self.y * other.z - self.z * other.y, self.z * other.x - other.z * self.x, self.x * other.y - self.y * other.x)

    def norm(self) -> float: return hypot(self.x, self.y, self.z)
    def norm_sq(self) -> float: return self.x*self.x + self.y*self.y + self.z*self.z
    def dist(self, other) -> float: return hypot(self.x-other.x, self.y-other.y, self.z-other.z)
    def dist_sq(self, other) -> float: dx, dy, dz = self.x-other.x, self.y-other.y, self.z-other.z; return dx*dx + dy*dy + dz*dz