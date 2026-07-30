pub assume_specification<T: ZeroablePrimitive>[ NonZero::<T>::new_unchecked ](n: T) -> (ret:
    NonZero<T>)
    requires
        !n.is_zero(),
    ensures
        ret@ == n,
    opens_invariants none
    no_unwind
;
