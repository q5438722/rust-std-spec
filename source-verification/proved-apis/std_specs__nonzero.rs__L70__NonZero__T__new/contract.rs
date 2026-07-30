pub assume_specification<T: ZeroablePrimitive>[ NonZero::<T>::new ](n: T) -> (ret: Option<
    NonZero<T>,
>)
    ensures
        match ret {
            Some(nz) => nz@ == n && !n.is_zero(),
            None => n.is_zero(),
        },
    opens_invariants none
    no_unwind
;
