pub assume_specification[ FromUtf8Error::as_bytes ](error: &FromUtf8Error) -> (result: &[u8])
    ensures
        result@ == error@.bytes,
;
