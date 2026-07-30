pub assume_specification[ Duration::checked_div ](lhs: Duration, rhs: u32) -> (result: Option<
    Duration,
>)
    ensures
        rhs != 0 ==> (result matches Some(value) && value@ == lhs@ / rhs as nat),
        rhs == 0 ==> result is None,
;
