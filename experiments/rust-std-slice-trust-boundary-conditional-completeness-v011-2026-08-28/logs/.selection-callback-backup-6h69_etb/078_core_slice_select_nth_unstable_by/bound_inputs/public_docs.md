Reorders the slice with a comparator function such that the element at `index` is at a
sort-order position. All elements before `index` will be `<=` to this value, and all
elements after will be `>=` to it, according to the comparator function.

This reordering is unstable (i.e. any element that compares equal to the nth element may end
up at that position), in-place (i.e.  does not allocate), and runs in *O*(*n*) time. This
function is also known as "kth element" in other libraries.

Returns a triple partitioning the reordered slice:

* The unsorted subslice before `index`, whose elements all satisfy
`compare(x, self[index]).is_le()`.

* The element at `index`.

* The unsorted subslice after `index`, whose elements all satisfy
`compare(x, self[index]).is_ge()`.

# Current implementation

The current algorithm is an introselect implementation based on [ipnsort] by Lukas Bergdoll
and Orson Peters, which is also the basis for [`sort_unstable`]. The fallback algorithm is
Median of Medians using Tukey's Ninther for pivot selection, which guarantees linear runtime
for all inputs.

[`sort_unstable`]: slice::sort_unstable

# Panics

Panics when `index >= len()`, and so always panics on empty slices.

May panic if `compare` does not implement a [total order].

# Examples

```
let mut v = [-5i32, 4, 2, -3, 1];

// Find the items `>=` to the median, the median itself, and the items `<=` to it, by using
// a reversed comparator.
let (before, median, after) = v.select_nth_unstable_by(2, |a, b| b.cmp(a));

assert!(before == [4, 2] || before == [2, 4]);
assert_eq!(median, &mut 1);
assert!(after == [-3, -5] || after == [-5, -3]);

// We are only guaranteed the slice will be one of the following, based on the way we sort
// about the specified index.
assert!(v == [2, 4, 1, -5, -3] ||
v == [2, 4, 1, -3, -5] ||
v == [4, 2, 1, -5, -3] ||
v == [4, 2, 1, -3, -5]);
```

[ipnsort]: https://github.com/Voultapher/sort-research-rs/tree/main/ipnsort
[total order]: https://en.wikipedia.org/wiki/Total_order
