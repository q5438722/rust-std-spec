pub assume_specification[ Duration::subsec_micros ](duration: &Duration) -> (result: u32)
    ensures
        result as nat == duration@ % nanos_per_second() / 1_000,
;
