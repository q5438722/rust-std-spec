pub assume_specification[ Duration::from_hours ](hours: u64) -> (result: Duration)
    requires
        hours as nat * 3_600 <= u64::MAX as nat,
    ensures
        result@ == hours as nat * 3_600 * nanos_per_second(),
;
