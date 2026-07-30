pub assume_specification<T, A: Allocator>[ Vec::<T, A>::push ](vec: &mut Vec<T, A>, value: T)
    ensures
        final(vec)@ == old(vec)@.push(value),
;
