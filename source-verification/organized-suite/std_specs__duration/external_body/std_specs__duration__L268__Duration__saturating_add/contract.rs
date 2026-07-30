pub assume_specification[ Duration::saturating_add ](lhs: Duration, rhs: Duration) -> (result:
    Duration)
    ensures
        result@ == if lhs@ + rhs@ <= duration_max_nanos() {
            lhs@ + rhs@
        } else {
            duration_max_nanos()
        },
;
