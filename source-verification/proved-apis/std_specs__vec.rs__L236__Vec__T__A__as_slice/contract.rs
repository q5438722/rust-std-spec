pub assume_specification<T, A: Allocator>[ Vec::<T, A>::as_slice ](vec: &Vec<T, A>) -> (slice: &[T])
    ensures
        slice@ == vec@,
;
