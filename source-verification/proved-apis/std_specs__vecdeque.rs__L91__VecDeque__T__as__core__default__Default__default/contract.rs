pub assume_specification<T>[ <VecDeque<T> as core::default::Default>::default ]() -> (v: VecDeque<
    T,
>)
    ensures
        v@ == Seq::<T>::empty(),
;
