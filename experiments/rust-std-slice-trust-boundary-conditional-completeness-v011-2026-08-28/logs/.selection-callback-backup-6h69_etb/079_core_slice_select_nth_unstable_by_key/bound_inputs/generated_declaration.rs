pub assume_specification<T, K: core::cmp::Ord, F: core::ops::FnMut(&T) -> K>[
    <[T]>::select_nth_unstable_by_key::<K, F>
](
    slice: &mut [T],
    index: usize,
    f: F,
) -> (ret: (&mut [T], &mut T, &mut [T]))
    requires
        index < old(slice)@.len(),
    ensures
        final(slice)@ == final(ret.0)@ + seq![*final(ret.1)] + final(ret.2)@,
        final(ret.0)@.len() == index,
        *final(ret.1) == final(slice)@[index as int],
        final(ret.2)@.len() == old(slice)@.len() - (index as int) - 1,
        slice_permutation(old(slice)@, final(slice)@),
        slice_select_partition_key::<F, T, K>(final(ret.0)@, *final(ret.1), final(ret.2)@, f),
;
