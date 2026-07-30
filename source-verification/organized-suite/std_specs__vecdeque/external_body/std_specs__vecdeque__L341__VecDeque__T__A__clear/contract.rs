pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::clear ](v: &mut VecDeque<T, A>)
    ensures
        final(v).view() == Seq::<T>::empty(),
;
