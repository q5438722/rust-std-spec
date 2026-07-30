pub assume_specification<B, C>[ ControlFlow::<B, C>::is_break ](
    value: &ControlFlow<B, C>,
) -> (result: bool)
    ensures
        result <==> value is Break,
;
