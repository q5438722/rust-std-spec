pub assume_specification[ str::from_utf8_unchecked ](v: &[u8]) -> (res: &str)
    requires
        valid_utf8(v@),
    ensures
        res.spec_bytes() =~= v@,
;
