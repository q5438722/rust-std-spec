pub assume_specification[ alloc::ffi::IntoStringError::into_cstring ](
    error: alloc::ffi::IntoStringError,
) -> (result: CString)
    ensures
        result@ == error@.value,
;
