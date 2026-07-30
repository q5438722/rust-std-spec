pub assume_specification<V: ?Sized>[ core::mem::size_of_val::<V> ](val: &V) -> (u: usize)
    ensures
        u as nat == spec_size_of_val::<V>(val),
    opens_invariants none
    no_unwind
;
