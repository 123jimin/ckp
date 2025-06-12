from collections import deque

def half_plane_intersection(half_planes: list[tuple[int, int, int]]) -> None|list[int]:
    """
        Computes the intersection of half-planes, where a half-plane ax + by >= c is given as a tuple (a, b, c).

        This function returns:
        - `None`, if the intersection is empty.
        - An empty list, if the intersection is the whole plane.
        - A list of indices of non-degenerate `half_planes` forming the intersection, ordered counter-clockwise.
    """

    pruned_half_planes = []
    for (a, b, c) in half_planes:
        if a == b == 0:
            if c > 0: return None
            continue
        pruned_half_planes.append((a, b, c))
    
    if not pruned_half_planes: return []
    if len(pruned_half_planes) == 1: return [0]
    
    raise NotImplementedError()