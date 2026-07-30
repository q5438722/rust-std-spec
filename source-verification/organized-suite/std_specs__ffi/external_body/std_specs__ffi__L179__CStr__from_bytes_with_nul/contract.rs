pub assume_specification[ CStr::from_bytes_with_nul ](bytes: &[u8]) -> (result: Result<
    &CStr,
    core::ffi::FromBytesWithNulError,
>)
    ensures
        c_string_bytes_with_nul_valid(bytes@) ==> (result matches Ok(value) && value@
            == bytes@.drop_last()),
        !c_string_bytes_with_nul_valid(bytes@) ==> result is Err,
;
