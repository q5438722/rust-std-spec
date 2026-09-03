Sorts the slice in ascending order **without** preserving the initial order of equal elements.

This sort is unstable (i.e., may reorder equal elements), in-place (i.e., does not
allocate), and *O*(*n* \* log(*n*)) worst-case.

If the implementation of [`Ord`] for `T` does not implement a [total order], the function
may panic; even if the function exits normally, the resulting order of elements in the slice
is unspecified. See also the note on panicking below.

For example `|a, b| (a - b).cmp(a)` is a comparison function that is neither transitive nor
reflexive nor total, `a < b < c < a` with `a = 1, b = 2, c = 3`. For more information and
examples see the [`Ord`] documentation.


All original elements will remain in the slice and any possible modifications via interior
mutability are observed in the input. Same is true if the implementation of [`Ord`] for `T` panics.

Sorting types that only implement [`PartialOrd`] such as [`f32`] and [`f64`] require
additional precautions. For example, `f32::NAN != f32::NAN`, which doesn't fulfill the
reflexivity requirement of [`Ord`]. By using an alternative comparison function with
`slice::sort_unstable_by` such as [`f32::total_cmp`] or [`f64::total_cmp`] that defines a
[total order] users can sort slices containing floating-point values. Alternatively, if all
values in the slice are guaranteed to be in a subset for which [`PartialOrd::partial_cmp`]
forms a [total order], it's possible to sort the slice with `sort_unstable_by(|a, b|
a.partial_cmp(b).unwrap())`.

# Current implementation

The current implementation is based on [ipnsort] by Lukas Bergdoll and Orson Peters, which
combines the fast average case of quicksort with the fast worst case of heapsort, achieving
linear time on fully sorted and reversed inputs. On inputs with k distinct elements, the
expected time to sort the data is *O*(*n* \* log(*k*)).

It is typically faster than stable sorting, except in a few special cases, e.g., when the
slice is partially sorted.

# Panics

May panic if the implementation of [`Ord`] for `T` does not implement a [total order], or if
the [`Ord`] implementation panics.

# Examples

```
let mut v = [4, -5, 1, -3, 2];

v.sort_unstable();
assert_eq!(v, [-5, -3, 1, 2, 4]);
```

[ipnsort]: https://github.com/Voultapher/sort-research-rs/tree/main/ipnsort
[total order]: https://en.wikipedia.org/wiki/Total_order
