pub assume_specification[ core::str::Utf8Error::error_len ](
    error: &core::str::Utf8Error,
) -> (result: Option<usize>)
    ensures
        result == error@.error_len,
;
