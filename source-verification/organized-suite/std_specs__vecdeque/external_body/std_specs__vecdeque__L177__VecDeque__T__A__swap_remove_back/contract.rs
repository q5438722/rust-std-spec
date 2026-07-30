pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::swap_remove_back ](
    v: &mut VecDeque<T, A>,
    index: usize,
) -> (result: Option<T>)
    ensures
        match result {
            Some(value) => {
                &&& index < old(v)@.len()
                &&& value == old(v)@[index as int]
                &&& final(v)@ == old(v)@.update(index as int, old(v)@.last()).drop_last()
            },
            None => {
                &&& old(v)@.len() <= index
                &&& final(v)@ == old(v)@
            },
        },
;
