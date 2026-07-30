pub assume_specification[ Duration::new ](secs: u64, nanos: u32) -> (result: Duration)
    requires
        secs as nat + nanos as nat / nanos_per_second() <= u64::MAX as nat,
    ensures
        result@ == secs as nat * nanos_per_second() + nanos as nat,
;
