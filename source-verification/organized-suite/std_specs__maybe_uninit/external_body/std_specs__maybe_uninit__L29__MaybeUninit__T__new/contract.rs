pub assume_specification<T>[ MaybeUninit::<T>::new ](val: T) -> (res: MaybeUninit<T>)
    ensures res.mem_contents() == MemContents::Init(val),
    opens_invariants none
    no_unwind;
