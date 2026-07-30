pub assume_specification[ CString::into_boxed_c_str ](value: CString) -> (result: Box<CStr>)
    ensures
        (*result)@ == value@,
;
