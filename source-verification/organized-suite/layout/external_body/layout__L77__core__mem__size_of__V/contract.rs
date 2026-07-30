pub assume_specification<V>[ core::mem::size_of::<V> ]() -> (u: usize)
    ensures
        u as nat == size_of::<V>(),
    opens_invariants none
    no_unwind
;
