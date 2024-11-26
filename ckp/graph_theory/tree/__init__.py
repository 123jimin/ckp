"""
    This package contains algorithms related to handling trees.
"""

from .tree import TreeData, tree_from_neighbors, tree_from_parents, tree_from_edges, tree_centroids
from .tree import DistanceTreeData, distance_tree_init, distance_tree_from_edges

from .isomorphism import rooted_tree_isomorphism_signature, rooted_tree_child_isomorphism_signatures, rooted_tree_is_isomorphic_to
from .isomorphism import tree_isomorphism_signature, tree_is_isomorphic_to

from .hld import tree_hld_init, tree_hld_decompose_descendant
from .lca import tree_lca_init, tree_lca_pth_ancestor, tree_lca_query