pub assume_specification[ CStr::to_bytes_with_nul ](value: &CStr) -> (result: &[u8])
    ensures
        result@ == value@.push(0),
;
