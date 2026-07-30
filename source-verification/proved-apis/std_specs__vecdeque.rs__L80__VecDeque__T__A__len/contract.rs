pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::len ](v: &VecDeque<T, A>) -> (len:
    usize)
    ensures
        len == spec_vec_dequeue_len(v),
;
