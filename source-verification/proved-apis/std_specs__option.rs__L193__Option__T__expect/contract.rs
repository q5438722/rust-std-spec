pub assume_specification<T>[ Option::<T>::expect ](option: Option<T>, msg: &str) -> (t: T)
    requires
        option is Some,
    ensures
        t == spec_expect(option, msg),
;
