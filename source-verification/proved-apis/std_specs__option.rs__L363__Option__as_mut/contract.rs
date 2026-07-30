pub assume_specification<T>[ Option::as_mut ](option: &mut Option<T>) -> (res: Option<&mut T>)
    ensures
        (match *old(option) {
            None => final(option).is_none() && res.is_none(),
            Some(r) => final(option).is_some() && res.is_some() && *res.unwrap() == r
                && *final(res.unwrap()) == final(option).unwrap(),
        }),
;
