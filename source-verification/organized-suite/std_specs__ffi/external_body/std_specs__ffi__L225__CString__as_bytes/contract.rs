pub assume_specification[ CString::as_bytes ](value: &CString) -> (result: &[u8])
    ensures
        result@ == value@,
;
