pub assume_specification<T>[ <[T]>::is_empty ](slice: &[T]) -> (b: bool)
    ensures
        b <==> slice@.len() == 0,
;
