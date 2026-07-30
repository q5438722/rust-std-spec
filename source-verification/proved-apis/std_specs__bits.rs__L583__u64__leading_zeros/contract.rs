pub assume_specification[ u64::leading_zeros ](i: u64) -> (r: u32)
    ensures
        r as int == u64_leading_zeros(i),
;
