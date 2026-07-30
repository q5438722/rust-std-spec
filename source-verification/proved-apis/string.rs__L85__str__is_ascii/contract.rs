pub assume_specification[ str::is_ascii ](s: &str) -> (b: bool)
    ensures
        b == is_ascii(s),
;
