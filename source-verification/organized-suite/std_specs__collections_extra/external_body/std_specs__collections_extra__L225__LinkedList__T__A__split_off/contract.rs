pub assume_specification<T, A: Allocator>[ LinkedList::<T, A>::split_off ](
    list: &mut LinkedList<T, A>,
    at: usize,
) -> (result: LinkedList<T, A>) where A: Clone
    requires
        at <= old(list)@.len(),
    ensures
        final(list)@ == old(list)@.take(at as int),
        result@ == old(list)@.skip(at as int),
;
