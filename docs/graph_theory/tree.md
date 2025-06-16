# Tree

`ckp.graph_theory.tree` contains implementations of algorithms on graphs.

## Tree Data

Tree-related algorithms revolve around the following data structure:

```py
class TreeData:
    root: int
    neighbors: list[list[int]]
    parents: list[int]
    depths: list[int]
    sizes: list[int]|None
    def __len__(self) -> int: pass
    def __repr__(self) -> int: pass

```

Each node of a tree is represented by an integer between 0 and `len(tree)-1`.

- `tree.root`: The root node of a tree. Typically `0`, but could be any other node.
- `tree.parents`: Parent of each node. The root node's parent is `-1`.
- `tree.depths`: Depth of each node. The root node's depth is `0`.
- `tree.sizes`: Size of subtree of each node.
  - This is not computed by default, and calling `tree_sizes(tree)` automatically sets `tree.sizes` if it does not exist.



### Distance Tree

## Lowest Common Ancestor

## Heavy-Light Decomposition
