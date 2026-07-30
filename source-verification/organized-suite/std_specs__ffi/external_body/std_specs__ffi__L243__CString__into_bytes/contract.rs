pub assume_specification[ CString::into_bytes ](value: CString) -> (result: Vec<u8>)
    ensures
        result@ == value@,
;
