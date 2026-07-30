pub assume_specification<T>[ Option::as_mut_slice ](option: &mut Option<T>) -> (res: &mut [T])
    ensures
        res@ == (match *old(option) {
            Some(x) => seq![x],
            None => seq![],
        }),
        final(res)@.len() == res@.len(),  // TODO this should be broadcast for all `&mut [T]`
        final(option)@ == (match *old(option) {
            Some(_) => Some(final(res)@[0]),
            None => None,
        }),
;
