pub assume_specification[ Duration::saturating_mul ](lhs: Duration, rhs: u32) -> (result: Duration)
    ensures
        result@ == if lhs@ * rhs as nat <= duration_max_nanos() {
            lhs@ * rhs as nat
        } else {
            duration_max_nanos()
        },
;
