pub assume_specification<T: PartialEq, A: Allocator>[ VecDeque::<T, A>::contains ](
    v: &VecDeque<T, A>,
    value: &T,
) -> (result: bool)
    requires
        T::obeys_eq_spec(),
    ensures
        result <==> exists|i: int| 0 <= i < v@.len() && #[trigger] v@[i].eq_spec(value),
;
