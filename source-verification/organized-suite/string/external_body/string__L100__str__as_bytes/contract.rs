pub assume_specification[ str::as_bytes ](s: &str) -> (b: &[u8])
    ensures
        b@ == s.spec_bytes(),
;
