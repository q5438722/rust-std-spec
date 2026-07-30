pub assume_specification<T>[ Option::<T>::is_some ](option: &Option<T>) -> (b: bool)
    ensures
        b == is_some(option),
    no_unwind
;
