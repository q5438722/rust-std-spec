pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::pop_front ](
    v: &mut VecDeque<T, A>,
) -> (value: Option<T>)
    ensures
        match value {
            Some(x) => {
                &&& old(v)@.len() > 0
                &&& x == old(v)@[0]
                &&& final(v)@ == old(v)@.subrange(1, old(v)@.len() as int)
            },
            None => {
                &&& old(v)@.len() == 0
                &&& final(v)@ == old(v)@
            },
        },
;
