pub assume_specification<T>[ Option::<T>::unwrap ](option: Option<T>) -> (t: T)
    requires
        option is Some,
    ensures
        t == spec_unwrap(option),
;
