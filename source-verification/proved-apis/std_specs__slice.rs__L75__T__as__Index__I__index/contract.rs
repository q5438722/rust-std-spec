pub assume_specification<T, I: SliceIndex<[T]>> [<[T] as Index<I>>::index] (
    slice: &[T],
    index: I,
) -> (output: &<I as core::slice::SliceIndex<[T]>>::Output)
    ensures
        call_ensures(<I as SliceIndex<[T]>>::index, (index, slice), output),
;
