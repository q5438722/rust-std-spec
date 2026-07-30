pub assume_specification[ CString::into_bytes_with_nul ](value: CString) -> (result: Vec<u8>)
    ensures
        result@ == value@.push(0),
;
