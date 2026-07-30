pub assume_specification[ CString::as_c_str ](value: &CString) -> (result: &CStr)
    ensures
        result@ == value@,
;
