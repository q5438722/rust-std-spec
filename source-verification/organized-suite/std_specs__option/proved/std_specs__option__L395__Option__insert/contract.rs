pub assume_specification<T>[ Option::insert ](option: &mut Option<T>, value: T) -> (res: &mut T)
    ensures
        *res == value,
        *final(option) == Some(*final(res)),
;
