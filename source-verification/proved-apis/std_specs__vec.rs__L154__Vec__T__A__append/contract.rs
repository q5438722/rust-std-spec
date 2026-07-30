pub assume_specification<T, A: Allocator>[ Vec::<T, A>::append ](
    vec: &mut Vec<T, A>,
    other: &mut Vec<T, A>,
)
    ensures
        final(vec)@ == old(vec)@ + old(other)@,
        final(other)@ == Seq::<T>::empty(),
;
