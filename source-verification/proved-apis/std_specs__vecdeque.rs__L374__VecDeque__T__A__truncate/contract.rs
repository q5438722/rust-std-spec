pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::truncate ](
    v: &mut VecDeque<T, A>,
    len: usize,
)
    ensures
        len <= old(v).len() ==> final(v)@ == old(v)@.subrange(0, len as int),
        len > old(v).len() ==> final(v)@ == old(v)@,
;
