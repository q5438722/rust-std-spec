pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::rotate_left ](
    v: &mut VecDeque<T, A>,
    mid: usize,
)
    requires
        mid <= old(v)@.len(),
    ensures
        final(v)@ == old(v)@.subrange(mid as int, old(v)@.len() as int) + old(v)@.subrange(
            0,
            mid as int,
        ),
;
