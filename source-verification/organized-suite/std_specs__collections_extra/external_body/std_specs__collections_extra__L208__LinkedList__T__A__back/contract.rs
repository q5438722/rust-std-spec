pub assume_specification<T, A: Allocator>[ LinkedList::<T, A>::back ](
    list: &LinkedList<T, A>,
) -> (result: Option<&T>)
    ensures
        list@.len() == 0 ==> result is None,
        list@.len() > 0 ==> (result matches Some(value) && *value == list@.last()),
;
