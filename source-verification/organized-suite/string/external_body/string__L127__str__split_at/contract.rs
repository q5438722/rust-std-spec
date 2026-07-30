pub assume_specification[ str::split_at ](s: &str, mid: usize) -> (res: (&str, &str))
    requires
        is_char_boundary(s.spec_bytes(), mid as int),
    ensures
        res.0.spec_bytes() =~= s.spec_bytes().subrange(0, mid as int),
        res.1.spec_bytes() =~= s.spec_bytes().subrange(mid as int, s.spec_bytes().len() as int),
;
