pub assume_specification<T, A: Allocator>[ <Vec<T, A> as core::ops::DerefMut>::deref_mut ](
    vec: &mut Vec<T, A>,
) -> (slice: &mut [T])
    ensures
        slice@ == old(vec)@,
        final(slice)@ == final(vec)@,
;
