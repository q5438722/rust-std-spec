pub open spec fn slice_multiplicity<T>(seq: Seq<T>, value: T) -> nat {
    seq.to_multiset().count(value)
}

pub open spec fn slice_permutation<T>(left: Seq<T>, right: Seq<T>) -> bool {
    left.len() == right.len() && forall|value: T|
        slice_multiplicity(left, value) == slice_multiplicity(right, value)
}

pub uninterp spec fn ord_cmp_observed<T: core::cmp::Ord>(
    left: T,
    right: T,
) -> core::cmp::Ordering;

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

pub uninterp spec fn fnmut_key_observed<F, T, B>(f: F, value: T) -> B;

pub open spec fn slice_binary_search_by_key_ordered<F, T, B: core::cmp::Ord>(
    seq: Seq<T>,
    f: F,
) -> bool {
    forall|i: int, j: int| 0 <= i <= j < seq.len()
        ==> ord_leq_observed(
            fnmut_key_observed::<F, T, B>(f, seq[i]),
            fnmut_key_observed::<F, T, B>(f, seq[j]),
        )
}

pub open spec fn slice_binary_search_by_key_equal_at<F, T, B: core::cmp::Ord>(
    seq: Seq<T>,
    key: B,
    f: F,
    index: usize,
) -> bool {
    index < seq.len()
        && ord_cmp_observed(fnmut_key_observed::<F, T, B>(f, seq[index as int]), key)

pub open spec fn slice_select_partition_key<F, T, K: core::cmp::Ord>(
    left: Seq<T>,
    pivot: T,
    right: Seq<T>,
    f: F,
) -> bool {
    (forall|i: int| 0 <= i < left.len()
        ==> ord_leq_observed(fnmut_key_observed::<F, T, K>(f, left[i]), fnmut_key_observed::<F, T, K>(f, pivot)))
        && (forall|i: int| 0 <= i < right.len()
            ==> ord_leq_observed(fnmut_key_observed::<F, T, K>(f, pivot), fnmut_key_observed::<F, T, K>(f, right[i])))
}
