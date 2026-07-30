pub assume_specification<T, A: Allocator + core::clone::Clone>[ VecDeque::<T, A>::split_off ](
    v: &mut VecDeque<T, A>,
    at: usize,
) -> (return_value: VecDeque<T, A>)
    requires
        at <= old(v)@.len(),
    ensures
        final(v)@ == old(v)@.subrange(0, at as int),
        return_value@ == old(v)@.subrange(at as int, old(v)@.len() as int),
;
