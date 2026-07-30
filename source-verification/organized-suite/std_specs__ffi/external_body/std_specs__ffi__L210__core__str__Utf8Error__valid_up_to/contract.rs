pub assume_specification[ core::str::Utf8Error::valid_up_to ](
    error: &core::str::Utf8Error,
) -> (result: usize)
    ensures
        result == error@.valid_up_to,
;
