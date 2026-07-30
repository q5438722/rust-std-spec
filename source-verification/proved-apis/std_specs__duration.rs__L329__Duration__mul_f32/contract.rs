pub assume_specification[ Duration::mul_f32 ](duration: Duration, rhs: f32) -> (result: Duration)
    requires
        duration_float_ieee_semantics(),
        duration_secs_f32_valid(rhs * duration_as_secs_f32(duration@)),
    ensures
        result@ == duration_from_secs_f32_nanos(rhs * duration_as_secs_f32(duration@)),
;
