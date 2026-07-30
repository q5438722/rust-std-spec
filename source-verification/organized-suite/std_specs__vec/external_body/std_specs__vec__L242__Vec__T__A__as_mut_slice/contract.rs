pub assume_specification<T, A: Allocator>[ Vec::<T, A>::as_mut_slice ](vec: &mut Vec<T, A>) -> (slice: &mut [T])
    ensures
        slice@ == old(vec)@,
        final(slice)@ == final(vec)@,
;
