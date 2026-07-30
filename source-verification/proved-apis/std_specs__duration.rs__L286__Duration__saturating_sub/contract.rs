pub assume_specification[ Duration::saturating_sub ](lhs: Duration, rhs: Duration) -> (result:
    Duration)
    ensures
        result@ == if lhs@ >= rhs@ {
            lhs@ - rhs@
        } else {
            0
        },
;
