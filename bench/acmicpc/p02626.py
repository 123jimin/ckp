from ckp.geometry import min_enclosing_circle
import random, sys, math
sys.setrecursionlimit(10_000_000)
N = 100000
points = []

def setup():
    global points
    
    random.seed(42)
    points = [(random.randint(-30000, 30000), random.randint(-30000, 30000)) for _ in range(N)]

def bench():
    a, (acx, acy), acr = min_enclosing_circle(points)

    assert(abs(acx/a - 163.008313) < 0.001)
    assert(abs(acy/a - 54.380628) < 0.001)
    assert(abs(math.sqrt(acr/a/a) - 42263.568380) < 0.001)
    
    return a, acr

tags = ['geometry', 'min_enclosing_circle']