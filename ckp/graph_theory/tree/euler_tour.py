from .tree import TreeData, tree_sizes

class EulerTourData:
    """ Represents an euler tour of a tree. """
    __slots__ = ('visits', 'begin', 'end')

    visits: list[int]
    """ List of nodes visited in the euler tour. """

    begin: list[int]
    """ Index of the first visit to each node. `[begin[node], end[node])` forms a half-open range representing the subtree rooted at the node. """

    # TODO: This is unnecessary because of `tree_sizes(tree)`. Remove it.
    end: list[int]
    """ One plus index of the last visit to each node. `[begin[node], end[node])` forms a half-open range representing the subtree rooted at the node. """

def _euler_tour_dfs(tour: EulerTourData, tree: TreeData, node: int):
    t = len(tour.visits)

    tour.visits.append(node)
    tour.begin[node] = t

    for ch in tree.children[node]:
        _euler_tour_dfs(tour, tree, ch)

    tour.end[node] = len(tour.visits)

def euler_tour(tree: TreeData) -> EulerTourData:
    """ Returns the euler tour of the given tree, visiting each node in DFS order. """

    tour = EulerTourData()
    tour.visits = []
    tour.begin = [-1] * len(tree)
    tour.end = [-1] * len(tree)
    _euler_tour_dfs(tour, tree, tree.root)

    return tour

def euler_tour_sorted(tree: TreeData) -> EulerTourData:
    """
        Returns the euler tour of the given tree, visiting each node in DFS order.
        This visits are sorted so that heavy paths (for HLD) always appear together in the visits.
    """

    N = len(tree)
    tree_children = tree.children
    sizes = tree_sizes(tree)
    get_size = sizes.__getitem__
    root = tree.root

    tour = EulerTourData()
    tour_visits = tour.visits = []
    tour_begin = tour.begin = [-1] * N
    tour_end = tour.end = [-1] * N

    stack = [root]
    while stack:
        v = stack.pop()

        tour_begin[v] = t = len(tour_visits)
        tour_end[v] = t + get_size(v)
        tour_visits.append(v)

        # `reversed` is added to maintain consistency with HLD (earlier child gets chosen first).
        stack.extend(sorted(reversed(tree_children[v]), key=get_size))

    return tour