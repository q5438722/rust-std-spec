pub assume_specification<T, A: Allocator + core::clone::Clone>[ Vec::<T, A>::split_off ](
    vec: &mut Vec<T, A>,
    at: usize,
) -> (return_value: Vec<T, A>)
    requires
        at <= old(vec)@.len(),
    ensures
        final(vec)@ == old(vec)@.subrange(0, at as int),
        return_value@ == old(vec)@.subrange(at as int, old(vec)@.len() as int),
;
