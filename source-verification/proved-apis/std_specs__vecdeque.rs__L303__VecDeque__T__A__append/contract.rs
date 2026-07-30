pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::append ](
    v: &mut VecDeque<T, A>,
    other: &mut VecDeque<T, A>,
)
    ensures
        final(v)@ == old(v)@ + old(other)@,
        final(other)@ == Seq::<T>::empty(),
;
