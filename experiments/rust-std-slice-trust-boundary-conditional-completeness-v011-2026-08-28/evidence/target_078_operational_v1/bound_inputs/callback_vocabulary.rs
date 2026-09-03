pub ghost struct ComparatorObservation<T> {
    pub domain: Seq<T>,
    pub trace_id: int,
}

pub uninterp spec fn comparator_ordering_observed<T>(
    observation: ComparatorObservation<T>,
    left: T,
    right: T,
) -> core::cmp::Ordering;

pub open spec fn comparator_leq_observed<T>(
    observation: ComparatorObservation<T>,
    left: T,
    right: T,
) -> bool {
    ordering_rank(comparator_ordering_observed(observation, left, right)) <= 0
}

pub open spec fn slice_sorted_by_cmp<T>(
    seq: Seq<T>,
    observation: ComparatorObservation<T>,
) -> bool {
    forall|i: int, j: int| 0 <= i <= j < seq.len()
        ==> comparator_leq_observed(observation, seq[i], seq[j])
}

pub uninterp spec fn comparator_observation<F, T>(
    compare: F,
    domain: Seq<T>,
) -> ComparatorObservation<T>;

pub broadcast axiom fn axiom_comparator_observation_domain<F, T>(compare: F, domain: Seq<T>)
    ensures
        #[trigger] comparator_observation::<F, T>(compare, domain).domain == domain,
;

pub broadcast axiom fn axiom_comparator_ordering_observed_reflexive<T>(
    observation: ComparatorObservation<T>,
    value: T,
)
    ensures
        #[trigger] comparator_ordering_observed(observation, value, value)
            == core::cmp::Ordering::Equal,
;

pub broadcast axiom fn axiom_comparator_ordering_observed_dual<T>(
    observation: ComparatorObservation<T>,
    left: T,
    right: T,
)
    ensures
        #[trigger] comparator_ordering_observed(observation, left, right)
            == core::cmp::Ordering::Less
            <==> comparator_ordering_observed(observation, right, left)
                == core::cmp::Ordering::Greater,
        comparator_ordering_observed(observation, left, right) == core::cmp::Ordering::Equal
            <==> comparator_ordering_observed(observation, right, left)
                == core::cmp::Ordering::Equal,
        comparator_ordering_observed(observation, left, right)
            == core::cmp::Ordering::Greater
            <==> comparator_ordering_observed(observation, right, left)
                == core::cmp::Ordering::Less,
;

pub broadcast axiom fn axiom_comparator_leq_observed_total<T>(
    observation: ComparatorObservation<T>,
    left: T,
    right: T,
)
    ensures
        #[trigger] comparator_leq_observed(observation, left, right)
            || comparator_leq_observed(observation, right, left),
;

pub broadcast axiom fn axiom_comparator_leq_observed_transitive<T>(
    observation: ComparatorObservation<T>,
    left: T,
    middle: T,
    right: T,
)
    ensures
        #[trigger] comparator_leq_observed(observation, left, middle)
            && #[trigger] comparator_leq_observed(observation, middle, right)
            ==> comparator_leq_observed(observation, left, right),
;

pub open spec fn slice_select_partition_cmp<T>(
    left: Seq<T>,
    pivot: T,
    right: Seq<T>,
    observation: ComparatorObservation<T>,
) -> bool {
    (forall|i: int| 0 <= i < left.len() ==> comparator_leq_observed(observation, left[i], pivot))
        && (forall|i: int| 0 <= i < right.len() ==> comparator_leq_observed(observation, pivot, right[i]))
}
