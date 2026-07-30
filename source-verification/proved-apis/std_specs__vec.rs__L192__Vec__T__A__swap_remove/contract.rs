pub assume_specification<T, A: Allocator>[ Vec::<T, A>::swap_remove ](
    vec: &mut Vec<T, A>,
    i: usize,
) -> (element: T)
    requires
        i < old(vec).len(),
    ensures
        element == old(vec)[i as int],
        final(vec)@ == old(vec)@.update(i as int, old(vec)@.last()).drop_last(),
;
