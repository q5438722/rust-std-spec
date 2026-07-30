pub assume_specification<T, A: Allocator>[ LinkedList::<T, A>::pop_back ](
    list: &mut LinkedList<T, A>,
) -> (result: Option<T>)
    ensures
        old(list)@.len() == 0 ==> result is None && final(list)@ == old(list)@,
        old(list)@.len() > 0 ==> (result matches Some(value) && value == old(list)@.last()
            && final(list)@ == old(list)@.drop_last()),
;
