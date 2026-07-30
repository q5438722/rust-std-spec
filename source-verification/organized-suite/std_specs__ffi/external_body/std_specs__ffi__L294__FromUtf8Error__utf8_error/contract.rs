pub assume_specification[ FromUtf8Error::utf8_error ](error: &FromUtf8Error) -> (result:
    core::str::Utf8Error)
    ensures
        result@ == error@.error,
;
