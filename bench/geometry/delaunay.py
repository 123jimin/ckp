import cProfile
from bench.util import bench
from ckp.geometry.delaunay import delaunay_triangulation

import random
random.seed(42)

N = 20_000
points = [(random.randrange(1_000_000_000), random.randrange(1_000_000_000)) for _ in range(N)]

def bench_delaunay_triangulation():
    res = sum(1 for _ in delaunay_triangulation(points))
    assert(res == 59976)

    return res

if __name__ == '__main__':
    bench([
        "bench_delaunay_triangulation()"
    ], num_trials=8, global_vars=globals())
    
    cProfile.run("[bench_delaunay_triangulation() for _ in range(5)]", sort='tottime')