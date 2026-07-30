pub assume_specification<T>[ MaybeUninit::<T>::assume_init_ref ](m: &MaybeUninit<T>) -> (ret: &T)
    requires m.mem_contents().is_init(),
    ensures ret == m.mem_contents().value(),
    opens_invariants none
    no_unwind;
