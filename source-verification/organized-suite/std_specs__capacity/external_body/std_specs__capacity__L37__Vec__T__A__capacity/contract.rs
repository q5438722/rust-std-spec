pub assume_specification<T, A: Allocator>[ Vec::<T, A>::capacity ](v: &Vec<T, A>) -> (result: usize)
    ensures
        result as nat == v.spec_capacity(),
;
