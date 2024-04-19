def convex_hull_andrew(points: list[tuple[int, int]]) -> list[int]:
    """ Implementation of Andrew's monotone chain algorithm."""

    if len(points) == 0: return []
    if len(points) == 1: return [0]
    if len(points) == 2: return [0, 1]

    points_i = sorted(range(len(points)), key=points.__getitem__)

    lower = []
    for i in points_i:
        px, py = points[i]
        while len(lower) >= 2:
            hx, hy = points[lower[-1]]
            phx, phy = points[lower[-2]]
            hx, hy = hx-phx, hy-phy
            rpx, rpy = px-phx, py-phy
            if hx*rpy - hy*rpx > 0: break
            lower.pop()
        lower.append(i)

    upper = []
    for i in reversed(points_i):
        px, py = points[i]
        while len(upper) >= 2:
            hx, hy = points[upper[-1]]
            phx, phy = points[upper[-2]]
            hx, hy = hx-phx, hy-phy
            rpx, rpy = px-phx, py-phy
            if hx*rpy - hy*rpx > 0: break
            upper.pop()
        upper.append(i)
    
    lower.pop(); upper.pop()
    lower.extend(upper)
    
    return lower

def convex_hull(points: list[tuple[int, int]]) -> list[int]:
    """ Given a list of points, returns indices of points forming the convex hull, in a counter-clockwise order. """
    return convex_hull_andrew(points)