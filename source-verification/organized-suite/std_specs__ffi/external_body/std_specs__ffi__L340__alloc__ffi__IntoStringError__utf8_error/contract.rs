pub assume_specification[ alloc::ffi::IntoStringError::utf8_error ](
    error: &alloc::ffi::IntoStringError,
) -> (result: core::str::Utf8Error)
    ensures
        result@ == error@.error,
;
