pub assume_specification<B, C>[ ControlFlow::<B, C>::break_value ](
    value: ControlFlow<B, C>,
) -> (result: Option<B>)
    ensures
        result == match value {
            ControlFlow::Break(b) => Some(b),
            ControlFlow::Continue(_) => None,
        },
;
