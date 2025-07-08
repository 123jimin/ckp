# Segment Tree

> Note: this submodule is work-in-progress.

CKP provides some generic implementations of segment trees, together with specialized implementations for several common cases.

For ease of use, `ckp.data_structure.segment_tree` uses object-oriented APIs.

## General Structure

Most segment trees' APIs look like a subset of this:

```py
class SegmentTree:
    def __init__(self, init_values: list|int, ...): pass
    def __len__(self) -> int: pass
    def __str__(self) -> str: pass
    def __iter__(self): pass

    def __getitem__(self, ind: int): pass
    def sum_range(self, start: int, end: int): pass
    def sum_all(self): pass

    def __setitem__(self, ind: int, value): pass
    def set_range(self, start: int, end: int, value): pass

    def add_to(self, ind: int, value): pass
    def add_to_range(self, start: int, end: int, value): pass

    def mul_to(self, ind: int, value): pass
    def mul_to_range(self, start: int, end: int, value): pass
    
    def mul_add_to(self, ind: int, m, d): pass
    def mul_add_to_range(self, start: int, end: int, m, d): pass
```

- `init_values` can either be `list` (the list of initial values), or `int` (the size of segment tree).
- All ranges are half-open; `(start, end)` represents elements such that its index $i$ satisfies $start \le i < end$.

The API does *not* make use of [slice objects](https://docs.python.org/3/glossary.html#term-slice), as using them induce significant overhead.

### Variations

A lot of competitive programming problems revolve around using segment trees in various ways.
Hence CKP provides many variations of segment trees.

This section describes different ways to classify segment trees.

#### Base Value Type

A segment tree can be based on a *monoid* or a *ring*, potentially non-commutative.

- A monoid is represented via a tuple `(op, zero)`.
- A ring is represented via a tuple `(op_add, op_mul, zero, one)`.

CKP also provides segment tree implementations specialized for specific monoids/rings:

| Prefix | Description |
| ------ | ----------- |
| (None) | Python's numeric type. (The ring `(+, *, 0, 1)`) |
| `Monoid` / `Ring` | An arbitrary monoid or ring. |
| `CommutativeMonoid` | A commutative monoid. |
| `Max` / `Min` | Monoids `(max, min_value)` and `(min, max_value)`. |
| `GCD` | The monoid `(math.gcd, 0)`. |

The numeric type is the most widely supported one.

#### Operation Types

An operation may be applied either on a range or an element.

For a segment tree on a monoid, there can be two kinds of operations:

- **Assign**: set `a[i]` to a certain value `v`.
- **Add**: `a[i] += d`; add-assign `d` to `a[i]`.

For a segment tree on a ring, these operations are possible:

- **Assign**: set `a[i]` to a certain value `v`.
- **Add**: `a[i] += d`; add-assign `d` to `a[i]`.
- **Multiply**: `a[i] *= m`; mul-assign `m` to `a[i]`.
- **Mul-Add**: `a[i] = a[i]*m + d`; multiply `m` and add `d` to `a[i]` .

For querying items and sum, these operations are possible:

- **Get Item**: get value of a single element `a[i]`.
- **Range Sum**: get range sum `sum(a[i:j])`.

Segment trees supporting larger sets of operations are slower, so there's a trade-off.

Check the 'Implementations' section for names of segment trees supporting specific subsets of these operations.

### Optimization

Segment trees with **Fast** prefixed are more optimized (inlined functions, etc...), but harder to customize, versions.

For most cases, the fast variants are not necessary.

## Implementations

Here are the tables of segment trees implemented by CKP.

### Monoid

- ❌: no support (linear runtime)
- ⚠️: single element support
- ✅: (range) support

| Name | `a[i] = v` | `a[i] += d` | Get `a[i]` | Sum `a[i:j]` |
| ---- | ---------- | ----------- | ---------- | ------------ |
| `list` (for comparison) | ⚠️ | ⚠️ | ✅ | ❌ |
| `MonoidSumSegmentTree` | ⚠️ | ⚠️ | ✅ | ✅ |
| `MonoidAddSegmentTree` | ⚠️ | ✅ | ✅ | ❌ |
| `MonoidSegmentTree` | ⚠️ | ✅ | ✅ | ✅ |
| `MonoidAssignSegmentTree` | ✅ | ⚠️ | ✅ | ✅ |

#### MonoidSumSegmentTree

| Name | Description |
| ---- | ----------- |
| `MonoidSumSegmentTree` | |
| `SumSegmentTree` | |
| `FastSumSegmentTree` | `SumSegmentTree` with inlined function calls. |
| `MaxSegmentTree` | |
| `GCDSegmentTree` | |

#### MonoidAddSegmentTree

| Name | Description |
| ---- | ----------- |
| ~~`MonoidAddSegmentTree`~~ | Not yet implemented. |
| `AddSegmentTree` | |

#### MonoidSegmentTree

| Name | Description |
| ---- | ----------- |
| ~~`MonoidSegmentTree`~~ | Not yet implemented. |
| `NumberSegmentTree` | |
| `FastNumberSegmentTree` | Faster but quite difficult to customize. |

#### MonoidAssignSegmentTree

### Ring

| Name | `a[i] = v` | `a[i] += d` | `a[i] *= d` | Get `a[i]` | Sum `a[i:j]` |
| ---- | ---------- | ----------- | ----------- | ---------- | ------------ |
| `list` | ⚠️ | ⚠️ | ⚠️ | ✅ | ❌ |
| `RingSegmentTree` | ✅ | ✅ | ✅ | ✅ | ✅ |

### Merge Sort

### Persistent

### Complete Binary Tree