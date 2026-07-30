pub assume_specification[ alloc::ffi::NulError::into_vec ](error: alloc::ffi::NulError) -> (result:
    Vec<u8>)
    ensures
        result@ == error@.bytes,
;
