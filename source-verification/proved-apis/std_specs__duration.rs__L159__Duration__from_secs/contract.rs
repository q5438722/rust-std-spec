pub assume_specification[ Duration::from_secs ](secs: u64) -> (result: Duration)
    ensures
        result@ == secs as nat * nanos_per_second(),
;
