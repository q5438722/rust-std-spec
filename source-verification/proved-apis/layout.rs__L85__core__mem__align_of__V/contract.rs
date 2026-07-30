pub assume_specification<V>[ core::mem::align_of::<V> ]() -> (u: usize)
    ensures
        u as nat == align_of::<V>(),
    opens_invariants none
    no_unwind
;
