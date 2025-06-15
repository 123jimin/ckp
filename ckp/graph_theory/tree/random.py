import random

from .tree import TreeData, tree_from_edges

def random_tree_edges(n: int) -> list[tuple[int, int]]:
    """ Generate edges for a random tree with `n` nodes. """
    perm = list(range(n))
    random.shuffle(perm)

    return [(perm[i], perm[random.randrange(i)]) for i in range(1, n)]

def random_tree(n: int) -> TreeData:
    """ Generate a random tree with `n` nodes, and with a randomly-chosen root. """
    return tree_from_edges(random_tree_edges(n), random.randrange(n))