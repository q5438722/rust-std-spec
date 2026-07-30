pub assume_specification<T, A: Allocator>[ Vec::<T, A>::new_in ](alloc: A) -> (v: Vec<T, A>)
    ensures
        v@ == Seq::<T>::empty(),
;
