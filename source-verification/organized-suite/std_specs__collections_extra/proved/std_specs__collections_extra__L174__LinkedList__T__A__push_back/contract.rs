pub assume_specification<T, A: Allocator>[ LinkedList::<T, A>::push_back ](
    list: &mut LinkedList<T, A>,
    item: T,
)
    ensures
        final(list)@ == old(list)@.push(item),
;
