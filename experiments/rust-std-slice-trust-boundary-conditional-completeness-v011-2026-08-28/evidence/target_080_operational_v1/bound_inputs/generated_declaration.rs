pub assume_specification<T: core::cmp::Ord>[ <[T]>::sort_unstable ](
    slice: &mut [T],
)
    ensures
        slice_permutation(old(slice)@, final(slice)@),
        slice_sorted_by_ord(final(slice)@),
;
