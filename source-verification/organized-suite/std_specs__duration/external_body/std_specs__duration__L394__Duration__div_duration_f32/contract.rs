pub assume_specification[ Duration::div_duration_f32 ](lhs: Duration, rhs: Duration) -> (result:
    f32)
    requires
        duration_float_ieee_semantics(),
    ensures
        lhs@ == 0 && rhs@ == 0 ==> result.is_nan_spec(),
        !(lhs@ == 0 && rhs@ == 0) ==> result == duration_as_nanos_f32(lhs@) / duration_as_nanos_f32(
            rhs@,
        ),
;
