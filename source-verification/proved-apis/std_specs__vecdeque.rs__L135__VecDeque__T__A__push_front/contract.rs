pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::push_front ](
    v: &mut VecDeque<T, A>,
    value: T,
)
    ensures
        final(v)@ == seq![value] + old(v)@,
;
