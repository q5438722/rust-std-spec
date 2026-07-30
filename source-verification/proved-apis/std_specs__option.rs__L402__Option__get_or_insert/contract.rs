pub assume_specification<T>[ Option::get_or_insert ](option: &mut Option<T>, value: T) -> (res:
    &mut T)
    ensures
        *res == (match *old(option) {
            Some(x) => x,
            None => value,
        }),
        *final(option) == Some(*final(res)),
;
