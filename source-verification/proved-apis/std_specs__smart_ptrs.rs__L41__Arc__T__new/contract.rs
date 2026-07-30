pub assume_specification<T>[ Arc::<T>::new ](t: T) -> (v: Arc<T>)
    ensures
        *v == t,
;
