pub assume_specification<T>[ core::mem::swap::<T> ](a: &mut T, b: &mut T)
    ensures
        *final(a) == *old(b),
        *final(b) == *old(a),
    opens_invariants none
    no_unwind
;
