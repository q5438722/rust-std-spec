pub broadcast axiom fn axiom_ord_cmp_observed_reflexive<T: core::cmp::Ord>(value: T)
    ensures
        #[trigger] ord_cmp_observed(value, value) == core::cmp::Ordering::Equal,
;

pub broadcast axiom fn axiom_ord_cmp_observed_dual<T: core::cmp::Ord>(left: T, right: T)
    ensures
        #[trigger] ord_cmp_observed(left, right) == core::cmp::Ordering::Less
            <==> ord_cmp_observed(right, left) == core::cmp::Ordering::Greater,
        ord_cmp_observed(left, right) == core::cmp::Ordering::Equal
            <==> ord_cmp_observed(right, left) == core::cmp::Ordering::Equal,
        ord_cmp_observed(left, right) == core::cmp::Ordering::Greater
            <==> ord_cmp_observed(right, left) == core::cmp::Ordering::Less,
;

pub broadcast axiom fn axiom_ord_cmp_observed_matches_partial_eq<T: core::cmp::Ord>(
    left: T,
    right: T,
)
    ensures
        #[trigger] ord_cmp_observed(left, right) == core::cmp::Ordering::Equal
            <==> partial_eq_observed(left, right),
;

pub open spec fn ordering_rank(ordering: core::cmp::Ordering) -> int {
    match ordering {
        core::cmp::Ordering::Less => -1,
        core::cmp::Ordering::Equal => 0,
        core::cmp::Ordering::Greater => 1,
    }
}

pub open spec fn ord_leq_observed<T: core::cmp::Ord>(left: T, right: T) -> bool {
    ordering_rank(ord_cmp_observed(left, right)) <= 0
}

pub broadcast axiom fn axiom_ord_leq_observed_total<T: core::cmp::Ord>(left: T, right: T)
    ensures
        #[trigger] ord_leq_observed(left, right) || ord_leq_observed(right, left),
;

pub broadcast axiom fn axiom_ord_leq_observed_transitive<T: core::cmp::Ord>(
    left: T,
    middle: T,
    right: T,
)
    ensures
        #[trigger] ord_leq_observed(left, middle) && #[trigger] ord_leq_observed(middle, right)
            ==> ord_leq_observed(left, right),
;
