pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::remove ](
    v: &mut VecDeque<T, A>,
    i: usize,
) -> (element: Option<T>)
    ensures
        match element {
            Some(x) => {
                &&& i < old(v)@.len()
                &&& x == old(v)@[i as int]
                &&& final(v)@ == old(v)@.remove(i as int)
            },
            None => {
                &&& old(v)@.len() <= i
                &&& final(v)@ == old(v)@
            },
        },
;
