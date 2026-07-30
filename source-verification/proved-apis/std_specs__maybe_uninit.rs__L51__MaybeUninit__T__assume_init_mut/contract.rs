pub assume_specification<T>[ MaybeUninit::<T>::assume_init_mut ](m: &mut MaybeUninit<T>) -> (ret: &mut T)
    requires m.mem_contents().is_init(),
    ensures *ret == old(m).mem_contents().value(),
        final(m).mem_contents().is_init(),
        final(m).mem_contents().value() == *final(ret),
    opens_invariants none
    no_unwind;
