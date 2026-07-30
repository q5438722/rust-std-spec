pub assume_specification[ Duration::mul_f64 ](duration: Duration, rhs: f64) -> (result: Duration)
    requires
        duration_float_ieee_semantics(),
        duration_secs_f64_valid(rhs * duration_as_secs_f64(duration@)),
    ensures
        result@ == duration_from_secs_f64_nanos(rhs * duration_as_secs_f64(duration@)),
;
