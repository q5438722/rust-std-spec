pub assume_specification<'a, T, A: Allocator>[ VecDeque::<T, A>::iter ](
    v: &'a VecDeque<T, A>,
) -> (iter: Iter<'a, T>)
    ensures
        iter == spec_iter(v),
        IteratorSpec::decrease(&iter) is Some,
        IteratorSpec::initial_value_relation(&iter, &iter),
;
