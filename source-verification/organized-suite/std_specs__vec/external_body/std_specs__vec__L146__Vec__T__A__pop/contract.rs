pub assume_specification<T, A: Allocator>[ Vec::<T, A>::pop ](vec: &mut Vec<T, A>) -> (value:
    Option<T>)
    ensures
        old(vec)@.len() > 0 ==> value == Some(old(vec)@[old(vec)@.len() - 1])
            && final(vec)@ == old(vec)@.subrange(0, old(vec)@.len() - 1),
        old(vec)@.len() == 0 ==> value == None::<T> && final(vec)@ == old(vec)@,
;
