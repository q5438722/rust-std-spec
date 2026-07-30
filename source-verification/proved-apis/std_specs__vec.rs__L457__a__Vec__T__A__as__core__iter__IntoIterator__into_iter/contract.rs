pub assume_specification<'a, T, A: Allocator> [<&'a Vec<T, A> as core::iter::IntoIterator>::into_iter] (vec: &'a Vec<T, A>) ->
    (iter: <&'a Vec<T, A> as core::iter::IntoIterator>::IntoIter)
    ensures
        iter == spec_into_iter_borrowed(vec),
        IteratorSpec::decrease(&iter) is Some,
        IteratorSpec::initial_value_relation(&iter, &iter),
;
