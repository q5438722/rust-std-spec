pub assume_specification[ CStr::from_bytes_until_nul ](bytes: &[u8]) -> (result: Result<
    &CStr,
    core::ffi::FromBytesUntilNulError,
>)
    ensures
        contains_nul(bytes@) ==> (result matches Ok(value) && value@ == bytes@.subrange(
            0,
            first_nul_index(bytes@),
        )),
        !contains_nul(bytes@) ==> result is Err,
;
