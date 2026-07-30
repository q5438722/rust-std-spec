pub assume_specification[ String::capacity ](s: &String) -> (result: usize)
    ensures
        result as nat == s.spec_capacity(),
;
