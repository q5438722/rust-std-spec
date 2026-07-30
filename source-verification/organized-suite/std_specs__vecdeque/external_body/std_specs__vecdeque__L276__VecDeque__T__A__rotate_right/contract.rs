pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::rotate_right ](
    v: &mut VecDeque<T, A>,
    k: usize,
)
    requires
        k <= old(v)@.len(),
    ensures
        final(v)@ == old(v)@.subrange(old(v)@.len() as int - k as int, old(v)@.len() as int) + old(
            v,
        )@.subrange(0, old(v)@.len() as int - k as int),
;
