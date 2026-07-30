pub assume_specification<T>[ Option::<T>::branch ](option: Option<T>) -> (cf: ControlFlow<
    <Option<T> as Try>::Residual,
    <Option<T> as Try>::Output,
>)
    ensures
        cf == match option {
            Some(v) => ControlFlow::Continue(v),
            None => ControlFlow::Break(None),
        },
    no_unwind
;
