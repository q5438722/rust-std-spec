pub assume_specification<T: Clone, A: Allocator>[ Vec::<T, A>::resize ](
    vec: &mut Vec<T, A>,
    len: usize,
    value: T,
)
    ensures
        len <= old(vec).len() ==> final(vec)@ == old(vec)@.subrange(0, len as int),
        len > old(vec).len() ==> {
            &&& final(vec)@.len() == len
            &&& final(vec)@.subrange(0, old(vec).len() as int) == old(vec)@
            &&& forall|i| #![all_triggers] old(vec).len() <= i < len ==> cloned::<T>(value, final(vec)@[i])
        },
;
