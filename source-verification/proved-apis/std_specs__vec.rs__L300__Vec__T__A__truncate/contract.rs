pub assume_specification<T, A: Allocator>[ Vec::<T, A>::truncate ](vec: &mut Vec<T, A>, len: usize)
    ensures
        len <= old(vec).len() ==> final(vec)@ == old(vec)@.subrange(0, len as int),
        len > old(vec).len() ==> final(vec)@ == old(vec)@,
;
