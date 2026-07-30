pub assume_specification<T>[ Option::as_slice ](option: &Option<T>) -> (res: &[T])
    ensures
        res@ == (match *option {
            Some(x) => seq![x],
            None => seq![],
        }),
;
