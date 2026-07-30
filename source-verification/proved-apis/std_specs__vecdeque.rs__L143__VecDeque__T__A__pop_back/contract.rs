pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::pop_back ](
    v: &mut VecDeque<T, A>,
) -> (value: Option<T>)
    ensures
        match value {
            Some(x) => {
                &&& old(v)@.len() > 0
                &&& x == old(v)@[old(v)@.len() - 1]
                &&& final(v)@ == old(v)@.subrange(0, old(v)@.len() as int - 1)
            },
            None => {
                &&& old(v)@.len() == 0
                &&& final(v)@ == old(v)@
            },
        },
;
