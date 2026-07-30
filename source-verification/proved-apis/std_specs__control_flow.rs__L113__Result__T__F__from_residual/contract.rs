pub assume_specification<T, E, F: From<E>>[ Result::<T, F>::from_residual ](
    result: Result<Infallible, E>,
) -> (result2: Result<T, F>)
    requires
        F::obeys_from_spec(),
    ensures
        match (result, result2) {
            (Err(e), Err(e2)) => e2 == F::from_spec(e),
            _ => false,
        },
;
