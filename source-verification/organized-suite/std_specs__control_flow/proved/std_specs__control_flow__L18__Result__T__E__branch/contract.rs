pub assume_specification<T, E>[ Result::<T, E>::branch ](result: Result<T, E>) -> (cf: ControlFlow<
    <Result<T, E> as Try>::Residual,
    <Result<T, E> as Try>::Output,
>)
    ensures
        cf == match result {
            Ok(v) => ControlFlow::Continue(v),
            Err(e) => ControlFlow::Break(Err(e)),
        },
    no_unwind
;
