pub assume_specification<T> [ <[T]>::last_mut ](slice: &mut [T]) -> (res: Option<&mut T>)
    ensures
        old(slice).len() == 0 ==> res.is_none() && final(slice)@ == seq![],
        old(slice).len() != 0 ==> res.is_some() && *res.unwrap() == old(slice)@.last()
            && final(slice)@ == old(slice)@.update(old(slice).len() - 1, *final(res.unwrap()))
;
