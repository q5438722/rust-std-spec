pub assume_specification[ CString::into_string ](value: CString) -> (result: Result<
    String,
    alloc::ffi::IntoStringError,
>)
    ensures
        valid_utf8(value@) ==> (result matches Ok(string) && string@ == decode_utf8(value@)),
        !valid_utf8(value@) ==> result is Err,
;
