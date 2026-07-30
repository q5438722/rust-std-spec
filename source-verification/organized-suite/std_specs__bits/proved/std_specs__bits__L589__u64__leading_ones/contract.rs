pub assume_specification[ u64::leading_ones ](i: u64) -> (r: u32)
    ensures
        r == u64_leading_ones(i),
;
