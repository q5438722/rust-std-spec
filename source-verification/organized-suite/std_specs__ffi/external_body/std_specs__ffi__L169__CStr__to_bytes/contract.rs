pub assume_specification[ CStr::to_bytes ](value: &CStr) -> (result: &[u8])
    ensures
        result@ == value@,
;
