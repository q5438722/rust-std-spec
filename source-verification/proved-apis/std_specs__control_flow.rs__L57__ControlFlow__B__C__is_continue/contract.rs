pub assume_specification<B, C>[ ControlFlow::<B, C>::is_continue ](
    value: &ControlFlow<B, C>,
) -> (result: bool)
    ensures
        result <==> value is Continue,
;
