pub assume_specification<T>[ ManuallyDrop::<T>::new ](value: T) -> (res: ManuallyDrop<T>)
    ensures
        res@ == value,
;
