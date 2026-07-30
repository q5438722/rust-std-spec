pub assume_specification<T, A: Allocator>[ Vec::<T, A>::into_iter ](vec: Vec<T, A>) -> (iter: <Vec<
    T,
    A,
> as core::iter::IntoIterator>::IntoIter)
    ensures
        iter == spec_into_iter(vec),
        IteratorSpec::decrease(&iter) is Some,
        IteratorSpec::initial_value_relation(&iter, &iter),
;
