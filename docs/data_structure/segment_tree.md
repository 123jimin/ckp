# Segment Tree

> Note: this submodule is work-in-progress.

CKP provides some generic implementations of segment trees, together with specialized implementations for several common cases.

For ease of use, `ckp.data_structure.segment_tree` uses object-oriented APIs.

## Classification

### Base

A segment tree can be based on a *monoid* or a *ring*, potentially non-commutative.

- A monoid is represented via a tuple `(zero, op)`.
- A ring is represented via a tuple `(zero, one, op_add, op_mul)`.

### Operation Types

An operation may be applied either on a range or an element.

For a segment tree on a monoid, there can be two kinds of operations:

- **Assign**: set `a[i]` to a certain value `v`.
- **Add**: `a[i] += d`; add-assign `d` to `a[i]`.

For a segment tree on a ring, these operations are possible:

- **Assign**: set `a[i]` to a certain value `v`.
- **Add**: `a[i] += d`; add-assign `d` to `a[i]`.
- **Multiply**: `a[i] *= m`; mul-assign `m` to `a[i]`.
- **Mul-Add**: `a[i] = a[i]*m + d`; multiply `m` and add `d` to `a[i]` .

### Query Types

- **Get Item**: get value of a single element `a[i]`.
- **Range Sum**: get range sum `sum(a[i:j])`.

There can be other types of operations, such as getting range max elements for a segment tree with the group of natural numbers with addition as the base monoid.

## Implementations

### Monoid

Here is the table of specific segment trees implemented by CKP.

- ❌: no support (linear runtime)
- ⚠️: single element support
- ✅: range support (for operations) / support (for query)

| Name | `a[i] = v` | `a[i] += d` | Get `a[i]` | Sum `a[i:j]` |
| ---- | ---------- | ----------- | ---------- | ------------ |
| `list` | ⚠️ | ⚠️ | ✅ | ❌ |
| `MonoidSumSegmentTree` | ⚠️ | ⚠️ | ✅ | ✅ |
| `MonoidAddSegmentTree` | ⚠️ | ✅ | ✅ | ❌ |
| `MonoidSegmentTree` | ✅ | ✅ | ✅ | ✅ |

There are some specialized instances for commonly occurring monoids:

- `MonoidSumSegmentTree`
  - `SumSegmentTree`
  - `MinSegmentTree`, `MaxSegmentTree`
  - `GCDSegmentTree`

### Merge Sort

### Persistent