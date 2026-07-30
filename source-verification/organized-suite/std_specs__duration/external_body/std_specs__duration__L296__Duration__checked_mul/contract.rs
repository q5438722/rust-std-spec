pub assume_specification[ Duration::checked_mul ](lhs: Duration, rhs: u32) -> (result: Option<
    Duration,
>)
    ensures
        lhs@ * rhs as nat <= duration_max_nanos() ==> (result matches Some(value) && value@ == lhs@
            * rhs as nat),
        lhs@ * rhs as nat > duration_max_nanos() ==> result is None,
;
