pub assume_specification<B, C>[ ControlFlow::<B, C>::continue_value ](
    value: ControlFlow<B, C>,
) -> (result: Option<C>)
    ensures
        result == match value {
            ControlFlow::Break(_) => None,
            ControlFlow::Continue(c) => Some(c),
        },
;
