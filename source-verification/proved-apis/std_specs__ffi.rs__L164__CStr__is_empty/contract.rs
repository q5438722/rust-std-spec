pub assume_specification[ CStr::is_empty ](value: &CStr) -> (result: bool)
    ensures
        result <==> value@.len() == 0,
;
