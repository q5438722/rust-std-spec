pub assume_specification[ Duration::from_mins ](mins: u64) -> (result: Duration)
    requires
        mins as nat * 60 <= u64::MAX as nat,
    ensures
        result@ == mins as nat * 60 * nanos_per_second(),
;
