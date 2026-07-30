pub assume_specification<T>[ Option::<T>::from_residual ](option: Option<Infallible>) -> (option2:
    Option<T>)
    ensures
        option.is_none(),
        option2.is_none(),
    no_unwind
;
