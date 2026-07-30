pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::as_slices ](
    v: &VecDeque<T, A>,
) -> (result: (&[T], &[T]))
    ensures
        result.0@ + result.1@ == v@,
;
