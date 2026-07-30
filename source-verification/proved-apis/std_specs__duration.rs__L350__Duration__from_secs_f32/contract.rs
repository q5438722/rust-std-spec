pub assume_specification[ Duration::from_secs_f32 ](secs: f32) -> (result: Duration)
    requires
        duration_secs_f32_valid(secs),
    ensures
        result@ == duration_from_secs_f32_nanos(secs),
;
