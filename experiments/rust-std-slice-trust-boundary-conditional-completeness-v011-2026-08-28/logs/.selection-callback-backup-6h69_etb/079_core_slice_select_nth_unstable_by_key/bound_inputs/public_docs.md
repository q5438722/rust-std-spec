Reorders the slice with a key extraction function such that the element at `index` is at a
sort-order position. All elements before `index` will have keys `<=` to the key at `index`,
and all elements after will have keys `>=` to it.

This reordering is unstable (i.e. any element that compares equal to the nth element may end
up at that position), in-place (i.e.  does not allocate), and runs in *O*(*n*) time. This
function is also known as "kth element" in other libraries.

Returns a triple partitioning the reordered slice:

* The unsorted subslice before `index`, whose elements all satisfy `f(x) <= f(self[index])`.

* The element at `index`.

* The unsorted subslice after `index`, whose elements all satisfy `f(x) >= f(self[index])`.

# Current implementation

The current algorithm is an introselect implementation based on [ipnsort] by Lukas Bergdoll
and Orson Peters, which is also the basis for [`sort_unstable`]. The fallback algorithm is
Median of Medians using Tukey's Ninther for pivot selection, which guarantees linear runtime
for all inputs.

[`sort_unstable`]: slice::sort_unstable

# Panics

Panics when `index >= len()`, meaning it always panics on empty slices.

May panic if `K: Ord` does not implement a total order.

# Examples

```
let mut v = [-5i32, 4, 1, -3, 2];

// Find the items `<=` to the absolute median, the absolute median itself, and the items
// `>=` to it.
let (lesser, median, greater) = v.select_nth_unstable_by_key(2, |a| a.abs());

assert!(lesser == [1, 2] || lesser == [2, 1]);
assert_eq!(median, &mut -3);
assert!(greater == [4, -5] || greater == [-5, 4]);

// We are only guaranteed the slice will be one of the following, based on the way we sort
// about the specified index.
assert!(v == [1, 2, -3, 4, -5] ||
v == [1, 2, -3, -5, 4] ||
v == [2, 1, -3, 4, -5] ||
v == [2, 1, -3, -5, 4]);
```

[ipnsort]: https://github.com/Voultapher/sort-research-rs/tree/main/ipnsort
[total order]: https://en.wikipedia.org/wiki/Total_order
