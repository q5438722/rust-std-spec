pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::push_back ](
    v: &mut VecDeque<T, A>,
    value: T,
)
    ensures
        final(v)@ == old(v)@.push(value),
;
