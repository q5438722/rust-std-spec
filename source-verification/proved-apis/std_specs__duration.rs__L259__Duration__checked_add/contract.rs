pub assume_specification[ Duration::checked_add ](lhs: Duration, rhs: Duration) -> (result: Option<
    Duration,
>)
    ensures
        lhs@ + rhs@ <= duration_max_nanos() ==> (result matches Some(value) && value@ == lhs@
            + rhs@),
        lhs@ + rhs@ > duration_max_nanos() ==> result is None,
;
