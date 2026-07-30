pub assume_specification[ CString::from_vec_with_nul ](bytes: Vec<u8>) -> (result: Result<
    CString,
    alloc::ffi::FromVecWithNulError,
>)
    ensures
        c_string_bytes_with_nul_valid(bytes@) ==> (result matches Ok(value) && value@
            == bytes@.drop_last()),
        !c_string_bytes_with_nul_valid(bytes@) ==> result is Err,
;
