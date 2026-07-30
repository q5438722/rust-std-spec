pub assume_specification<T>[ MaybeUninit::<T>::assume_init ](m: MaybeUninit<T>) -> T
    requires m.mem_contents().is_init(),
    returns m.mem_contents().value(),
    opens_invariants none
    no_unwind;
