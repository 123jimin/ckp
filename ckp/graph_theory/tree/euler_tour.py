from .tree import TreeData

class EulerTourData:
    """ Represents an euler tour of a tree. """
    __slots__ = ('visits', 'begin', 'end')

    visits: list[int]
    """ List of nodes visited in the euler tour. """

    begin: list[int]
    """ Index of the first visit to each node. `[begin[node], end[node])` forms a half-open range representing the subtree rooted at the node. """

    end: list[int]
    """ One plus index of the last visit to each node. `[begin[node], end[node])` forms a half-open range representing the subtree rooted at the node. """

def _euler_tour_dfs(tour: EulerTourData, tree: TreeData, node: int, parent: int):
    t = len(tour.visits)

    tour.visits.append(node)
    tour.begin[node] = t

    for ch in tree.neighbors[node]:
        if ch == parent: continue
        _euler_tour_dfs(tour, tree, ch, node)

    tour.end[node] = len(tour.visits)

def euler_tour(tree: TreeData) -> EulerTourData:
    """ Returns the euler tour of the given tree, visiting each node in DFS order. """

    tour = EulerTourData()
    tour.visits = []
    tour.begin = [-1] * len(tree)
    tour.end = [-1] * len(tree)
    _euler_tour_dfs(tour, tree, tree.root, -1)

    return tour

def _euler_tour_sorted_dfs(tour: EulerTourData, tree: TreeData, node: int, parent: int):
    # TODO
    raise NotImplementedError("Not yet implemented!")

def euler_tour_sorted(tree: TreeData) -> EulerTourData:
    """
        Returns the euler tour of the given tree, visiting each node in DFS order.
        This visits are sorted so that heavy paths (for HLD) always appear together in the visits.
    """

    tour = EulerTourData()
    tour.visits = []
    tour.begin = [-1] * len(tree)
    tour.end = [-1] * len(tree)
    _euler_tour_sorted_dfs(tour, tree, tree.root, -1)

    return tour