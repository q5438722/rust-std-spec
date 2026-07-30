pub assume_specification<T>[ Option::<T>::is_none ](option: &Option<T>) -> (b: bool)
    ensures
        b == is_none(option),
    no_unwind
;
