pub assume_specification[ Duration::abs_diff ](lhs: Duration, rhs: Duration) -> (result: Duration)
    ensures
        result@ == if lhs@ >= rhs@ {
            lhs@ - rhs@
        } else {
            rhs@ - lhs@
        },
;
