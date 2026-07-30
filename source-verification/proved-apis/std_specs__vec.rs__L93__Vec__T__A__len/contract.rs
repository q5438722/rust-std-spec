pub assume_specification<T, A: Allocator>[ Vec::<T, A>::len ](vec: &Vec<T, A>) -> (len: usize)
    ensures
        len == spec_vec_len(vec),
    no_unwind
;
