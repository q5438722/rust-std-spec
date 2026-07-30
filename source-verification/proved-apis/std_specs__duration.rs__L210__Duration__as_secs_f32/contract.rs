pub assume_specification[ Duration::as_secs_f32 ](duration: &Duration) -> (result: f32)
    requires
        duration_float_ieee_semantics(),
    ensures
        result == duration_as_secs_f32(duration@),
;
