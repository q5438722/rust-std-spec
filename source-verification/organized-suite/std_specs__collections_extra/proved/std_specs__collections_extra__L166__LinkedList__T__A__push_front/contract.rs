pub assume_specification<T, A: Allocator>[ LinkedList::<T, A>::push_front ](
    list: &mut LinkedList<T, A>,
    item: T,
)
    ensures
        final(list)@ == seq![item] + old(list)@,
;
