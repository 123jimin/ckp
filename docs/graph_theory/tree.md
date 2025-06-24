# Tree

`ckp.graph_theory.tree` contains implementations of algorithms on graphs.

Unless noted otherwise, all tree-related functions **don't recurse**, so the stack will *not* overflow even for large trees!

## Tree Data

Tree-related algorithms revolve around the following data structure:

```py
class TreeData:
    root: int
    parents: list[int]
    children: list[list[int]]
    depths: list[int]
    sizes: list[int]|None
    def __len__(self) -> int: pass
    def __repr__(self) -> int: pass

```

Each node of a tree is represented by an integer between 0 and `len(tree)-1`.

- `tree.root`: The root node of a tree. Typically `0`, but could be any other node.
- `tree.parents`: Parent of each node. The root node's parent is `-1`.
- `tree.children`: Children of each node.
- `tree.depths`: Depth of each node. The root node's depth is `0`.
- `tree.sizes`: Size of subtree of each node.
  - This is not computed by default, and calling `tree_sizes(tree)` automatically sets `tree.sizes` if it does not exist.

> `def tree_from_neighbors(neighbors: list[list[int]], root: int = 0) -> TreeData`

Create a `TreeData`, given a bi-directional adjacency list.

> `def tree_from_parents(parents: list[int], root: int = 0) -> TreeData`

Create a `TreeData`, given a list of parents.

> `def tree_from_edges(edges: list[tuple[int, int]], root: int = 0) -> TreeData`

Create a `TreeData`, given a list of edges. This is probably the most common way to create a tree.

> `def tree_with_root(tree: TreeData, new_root: int) -> TreeData`

Re-root the given tree.

> `def tree_sizes(tree: TreeData) -> list[int]`

Return `tree.sizes`, size of subtree for each node. If it's missing, then compute the list and cache it to `tree`.

## Centroids

> `def tree_centroids(tree: TreeData) -> list[int]`

Returns the centroid (or centroids) of the tree.

A centroid is a a vertex whose largest subtree has at most `len(tree) // 2` vertices.

A tree either has one or two centroids, so this function always return a list of one or two vertices (as long as the tree is non-empty).

## Lowest Common Ancestor

> `def tree_lca_init(tree: TreeData) -> TreeLCAData`

Pre-compute ancestor information for `tree`.

> `def tree_lca_pth_ancestor(lca: TreeLCAData, v: int, p: int) -> int`

Return the `p`-th ancestor of `v`.

> `def tree_lca_query(lca: TreeLCAData, v: int, w: int) -> int`

Return the lowest common ancestor of `v` and `w` using the pre-computed data.

## Heavy-Light Decomposition

```py
class TreeHLDData:
  path_index: list[tuple[int, int]]
  paths: list[list[int]]
```

> `def tree_hld_init(tree: TreeData) -> TreeHLDData`

> `def tree_hld_decompose_descendant(hld: TreeHLDData, node: int, ancestor: int)`

## Euler Tour

> `def euler_tour(tree: TreeData) -> EulerTourData`

Return an Euler tour of `tree`.  `tour.visits` lists the nodes in DFS order and `tour.begin[v]` gives the index of the first visit to `v`.

> `def euler_tour_sorted(tree: TreeData) -> EulerTourData`

Similar to `euler_tour` but children are visited in an order suitable for heavy-light decomposition so that nodes in the same heavy path appear consecutively in the tour.

## Tree Isomorphism

WARNING: The current implementation of tree isomorphism related functions **do recurse**, and very inefficient (while ensuring linear runtime).

> `def rooted_tree_isomorphism_signature(tree: TreeData) -> int`

> `def rooted_tree_is_isomorphic_to(a: TreeData, b: TreeData) -> bool`

Compute an isomorphism signature for a rooted tree and test whether two rooted trees are isomorphic.

> `def tree_isomorphism_signature(tree: TreeData) -> int`

> `def tree_is_isomorphic_to(a: TreeData, b: TreeData) -> bool`

Functions for un-rooted trees.  Centroids are chosen automatically and their signatures are compared.
