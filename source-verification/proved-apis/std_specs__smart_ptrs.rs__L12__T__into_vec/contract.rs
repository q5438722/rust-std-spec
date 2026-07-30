pub assume_specification<T, A: Allocator>[ <[T]>::into_vec ](b: Box<[T], A>) -> (v: Vec<T, A>)
    ensures
        v@ == b@,
;
