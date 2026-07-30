pub assume_specification<T, A: Allocator>[ LinkedList::<T, A>::clear ](list: &mut LinkedList<T, A>)
    ensures
        final(list)@ == Seq::<T>::empty(),
;
