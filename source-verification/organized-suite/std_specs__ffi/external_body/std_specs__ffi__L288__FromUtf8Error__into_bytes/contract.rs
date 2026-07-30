pub assume_specification[ FromUtf8Error::into_bytes ](error: FromUtf8Error) -> (result: Vec<u8>)
    ensures
        result@ == error@.bytes,
;
