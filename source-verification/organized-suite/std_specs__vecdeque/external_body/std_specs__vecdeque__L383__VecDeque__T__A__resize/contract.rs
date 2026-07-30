pub assume_specification<T: Clone, A: Allocator>[ VecDeque::<T, A>::resize ](
    v: &mut VecDeque<T, A>,
    len: usize,
    value: T,
)
    ensures
        len <= old(v).len() ==> final(v)@ == old(v)@.subrange(0, len as int),
        len > old(v).len() ==> {
            &&& final(v)@.len() == len
            &&& final(v)@.subrange(0, old(v).len() as int) == old(v)@
            &&& forall|i|
                #![all_triggers]
                old(v).len() <= i < len ==> cloned::<T>(value, final(v)@[i])
        },
;
