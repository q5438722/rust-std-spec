pub assume_specification<T, A: Allocator>[ Vec::<T, A>::with_capacity_in ](capacity: usize, alloc: A) -> (v: Vec<T, A>)
    ensures
        v@ == Seq::<T>::empty(),
;
