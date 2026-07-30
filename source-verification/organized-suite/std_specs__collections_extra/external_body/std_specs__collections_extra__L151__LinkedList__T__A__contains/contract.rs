pub assume_specification<T, A: Allocator>[ LinkedList::<T, A>::contains ](
    list: &LinkedList<T, A>,
    value: &T,
) -> (result: bool) where T: core::cmp::PartialEq<T>
    requires
        obeys_concrete_eq::<T>(),
    ensures
        result <==> list@.contains(*value),
;
