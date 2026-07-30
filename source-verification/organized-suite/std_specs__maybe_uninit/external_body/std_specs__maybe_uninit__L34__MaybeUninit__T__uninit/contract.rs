pub assume_specification<T>[ MaybeUninit::<T>::uninit ]() -> (res: MaybeUninit<T>)
    ensures res.mem_contents() == MemContents::Uninit,
    opens_invariants none
    no_unwind;
