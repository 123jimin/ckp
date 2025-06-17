from .tree import TreeData, tree_sizes

class EulerTourData:
    """ Represents an euler tour of a tree. """
    __slots__ = ('visits', 'begin')

    visits: list[int]
    """ List of nodes visited in the euler tour. """

    begin: list[int]
    """ Index of the first visit to each node. For all vertex `v`, `visits[begin[v]] == v` is true. """

def euler_tour(tree: TreeData) -> EulerTourData:
    """ Returns the euler tour of the given tree, visiting each node in DFS order. """

    tree_children = tree.children

    tour = EulerTourData()
    tour_visits = tour.visits = []
    tour_begin = tour.begin = [-1] * len(tree)

    stack = [tree.root]
    while stack:
        v = stack.pop()

        tour_begin[v] = len(tour_visits)
        tour_visits.append(v)

        stack.extend(reversed(tree_children[v]))

    return tour

def euler_tour_sorted(tree: TreeData) -> EulerTourData:
    """
        Returns the euler tour of the given tree, visiting each node in DFS order.
        This visits are sorted so that heavy paths (for HLD) always appear together in the visits.
    """

    tree_children = tree.children
    sizes = tree_sizes(tree)
    get_size = sizes.__getitem__

    tour = EulerTourData()
    tour_visits = tour.visits = []
    tour_begin = tour.begin = [-1] * len(tree)

    stack = [tree.root]
    while stack:
        v = stack.pop()

        tour_begin[v] = len(tour_visits)
        tour_visits.append(v)

        # `reversed` is added to maintain consistency with HLD (earlier child gets chosen first).
        stack.extend(sorted(reversed(tree_children[v]), key=get_size))

    return tour