pub assume_specification[ Duration::checked_sub ](lhs: Duration, rhs: Duration) -> (result: Option<
    Duration,
>)
    ensures
        lhs@ >= rhs@ ==> (result matches Some(value) && value@ == lhs@ - rhs@),
        lhs@ < rhs@ ==> result is None,
;
