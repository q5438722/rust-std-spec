pub assume_specification[ alloc::ffi::NulError::nul_position ](
    error: &alloc::ffi::NulError,
) -> (result: usize)
    ensures
        result == error@.position,
;
