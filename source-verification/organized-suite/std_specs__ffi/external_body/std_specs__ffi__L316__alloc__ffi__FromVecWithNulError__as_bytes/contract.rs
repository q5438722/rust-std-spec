pub assume_specification[ alloc::ffi::FromVecWithNulError::as_bytes ](
    error: &alloc::ffi::FromVecWithNulError,
) -> (result: &[u8])
    ensures
        result@ == error@,
;
