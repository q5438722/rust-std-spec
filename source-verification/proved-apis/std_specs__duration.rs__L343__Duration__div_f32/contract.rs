pub assume_specification[ Duration::div_f32 ](duration: Duration, rhs: f32) -> (result: Duration)
    requires
        duration_float_ieee_semantics(),
        duration_secs_f32_valid(duration_as_secs_f32(duration@) / rhs),
    ensures
        result@ == duration_from_secs_f32_nanos(duration_as_secs_f32(duration@) / rhs),
;
