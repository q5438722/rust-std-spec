pub assume_specification<T, A: Allocator>[ LinkedList::<T, A>::is_empty ](
    list: &LinkedList<T, A>,
) -> (result: bool)
    ensures
        result <==> list@.len() == 0,
;
