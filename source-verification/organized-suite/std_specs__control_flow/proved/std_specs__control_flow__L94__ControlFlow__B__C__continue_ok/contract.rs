pub assume_specification<B, C>[ ControlFlow::<B, C>::continue_ok ](
    value: ControlFlow<B, C>,
) -> (result: Result<C, B>)
    ensures
        result == match value {
            ControlFlow::Break(b) => Err(b),
            ControlFlow::Continue(c) => Ok(c),
        },
;
