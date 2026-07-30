pub assume_specification[ CString::as_bytes_with_nul ](value: &CString) -> (result: &[u8])
    ensures
        result@ == value@.push(0),
;
