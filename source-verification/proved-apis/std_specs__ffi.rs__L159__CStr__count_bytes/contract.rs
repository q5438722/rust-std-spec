pub assume_specification[ CStr::count_bytes ](value: &CStr) -> (result: usize)
    ensures
        result as nat == value@.len(),
;
