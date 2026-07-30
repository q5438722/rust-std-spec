pub assume_specification<T, A: Allocator>[ LinkedList::<T, A>::len ](
    list: &LinkedList<T, A>,
) -> (result: usize)
    ensures
        result as nat == list@.len(),
;
