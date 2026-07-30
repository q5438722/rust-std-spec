pub assume_specification<B, C>[ ControlFlow::<B, C>::break_ok ](
    value: ControlFlow<B, C>,
) -> (result: Result<B, C>)
    ensures
        result == match value {
            ControlFlow::Break(b) => Ok(b),
            ControlFlow::Continue(c) => Err(c),
        },
;
