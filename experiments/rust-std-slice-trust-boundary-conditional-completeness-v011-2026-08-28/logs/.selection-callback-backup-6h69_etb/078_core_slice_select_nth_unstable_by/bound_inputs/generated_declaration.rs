pub assume_specification<T, F: core::ops::FnMut(&T, &T) -> core::cmp::Ordering>[
    <[T]>::select_nth_unstable_by::<F>
](
    slice: &mut [T],
    index: usize,
    compare: F,
) -> (ret: (&mut [T], &mut T, &mut [T]))
    requires
        index < old(slice)@.len(),
    ensures
        final(slice)@ == final(ret.0)@ + seq![*final(ret.1)] + final(ret.2)@,
        final(ret.0)@.len() == index,
        *final(ret.1) == final(slice)@[index as int],
        final(ret.2)@.len() == old(slice)@.len() - (index as int) - 1,
        slice_permutation(old(slice)@, final(slice)@),
        slice_select_partition_cmp(
            final(ret.0)@,
            *final(ret.1),
            final(ret.2)@,
            comparator_observation(compare, old(slice)@),
        ),
;
