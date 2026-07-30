pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::insert ](
    v: &mut VecDeque<T, A>,
    i: usize,
    element: T,
)
    requires
        i <= old(v).len(),
    ensures
        final(v)@ == old(v)@.insert(i as int, element),
;
