pub assume_specification[ Duration::div_f64 ](duration: Duration, rhs: f64) -> (result: Duration)
    requires
        duration_float_ieee_semantics(),
        duration_secs_f64_valid(duration_as_secs_f64(duration@) / rhs),
    ensures
        result@ == duration_from_secs_f64_nanos(duration_as_secs_f64(duration@) / rhs),
;
