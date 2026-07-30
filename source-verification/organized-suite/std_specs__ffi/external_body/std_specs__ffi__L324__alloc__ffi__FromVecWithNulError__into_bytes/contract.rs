pub assume_specification[ alloc::ffi::FromVecWithNulError::into_bytes ](
    error: alloc::ffi::FromVecWithNulError,
) -> (result: Vec<u8>)
    ensures
        result@ == error@,
;
