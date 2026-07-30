pub assume_specification<T>[ Option::<T>::take ](option: &mut Option<T>) -> (t: Option<T>)
    ensures
        t == *old(option),
        *final(option) is None,
    no_unwind
;
