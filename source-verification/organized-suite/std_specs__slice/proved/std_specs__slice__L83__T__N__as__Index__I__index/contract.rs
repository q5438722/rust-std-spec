pub assume_specification<T, I, const N: usize> [<[T; N] as Index<I>>::index] (
    array: &[T; N],
    index: I,
) -> (output: &<[T; N] as core::ops::Index<I>>::Output)
    where [T]: Index<I>,
    ensures
        call_ensures(<[T] as Index<I>>::index, (array, index), output),
;
