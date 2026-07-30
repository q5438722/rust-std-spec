pub assume_specification[ CStr::to_str ](value: &CStr) -> (result: Result<
    &str,
    core::str::Utf8Error,
>)
    ensures
        valid_utf8(value@) ==> (result matches Ok(string) && string@ == decode_utf8(value@)),
        !valid_utf8(value@) ==> result is Err,
;
