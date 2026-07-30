pub assume_specification<T> [ <[T]>::last ](slice: &[T]) -> (res: Option<&T>)
    ensures
        slice.len() == 0 ==> res.is_none(),
        slice.len() != 0 ==> res.is_some() && res.unwrap() == slice@.last()
;
