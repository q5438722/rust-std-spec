pub assume_specification[ Duration::as_secs_f64 ](duration: &Duration) -> (result: f64)
    requires
        duration_float_ieee_semantics(),
    ensures
        result == duration_as_secs_f64(duration@),
;
