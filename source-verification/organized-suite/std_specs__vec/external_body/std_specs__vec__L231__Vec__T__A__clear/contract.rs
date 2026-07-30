pub assume_specification<T, A: Allocator>[ Vec::<T, A>::clear ](vec: &mut Vec<T, A>)
    ensures
        final(vec).view() == Seq::<T>::empty(),
;
