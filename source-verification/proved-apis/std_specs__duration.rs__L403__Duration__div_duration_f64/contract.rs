pub assume_specification[ Duration::div_duration_f64 ](lhs: Duration, rhs: Duration) -> (result:
    f64)
    requires
        duration_float_ieee_semantics(),
    ensures
        lhs@ == 0 && rhs@ == 0 ==> result.is_nan_spec(),
        !(lhs@ == 0 && rhs@ == 0) ==> result == duration_as_nanos_f64(lhs@) / duration_as_nanos_f64(
            rhs@,
        ),
;
