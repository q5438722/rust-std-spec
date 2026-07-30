pub assume_specification<T, A: Allocator>[ Vec::<T, A>::insert ](
    vec: &mut Vec<T, A>,
    i: usize,
    element: T,
)
    requires
        i <= old(vec).len(),
    ensures
        final(vec)@ == old(vec)@.insert(i as int, element),
;
