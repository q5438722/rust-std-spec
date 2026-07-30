pub assume_specification[ Duration::from_secs_f64 ](secs: f64) -> (result: Duration)
    requires
        duration_secs_f64_valid(secs),
    ensures
        result@ == duration_from_secs_f64_nanos(secs),
;
