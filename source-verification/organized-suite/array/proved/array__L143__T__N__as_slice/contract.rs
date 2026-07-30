pub assume_specification<T, const N: usize>[ <[T; N]>::as_slice ](ar: &[T; N]) -> (out: &[T])
    ensures
        ar@ == out@,
;
