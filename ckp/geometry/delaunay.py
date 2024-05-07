from ..data_structure.graph import UndirectedListGraph 
from .circumcircle import is_in_circumcircle, circumcircle_of_triangle
from .vector import Vec2

def _is_in_triangle_circumcircle(p1: Vec2, p2: Vec2, p3: Vec2, q: Vec2):
    return is_in_circumcircle(circumcircle_of_triangle([tuple(p1), tuple(p2), tuple(p3)]), tuple(q))

def delaunay_triangulation(points: list[Vec2|tuple[float|int, float|int]]) -> UndirectedListGraph:
    if len(points) < 2: return UndirectedListGraph(len(points))
    if len(points) == 2:
        graph = UndirectedListGraph(len(points))
        graph.add_edge(0, 1)
        return graph
    
    if not isinstance(points[0], Vec2): points = [Vec2(x, y) for (x, y) in points]

    raise Exception("Not yet implemented!")