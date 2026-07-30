pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::swap ](
    v: &mut VecDeque<T, A>,
    i: usize,
    j: usize,
)
    requires
        i < old(v)@.len(),
        j < old(v)@.len(),
    ensures
        final(v)@ == old(v)@.update(i as int, old(v)@[j as int]).update(
            j as int,
            old(v)@[i as int],
        ),
;
