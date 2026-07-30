pub assume_specification<T>[ Rc::<T>::new ](t: T) -> (v: Rc<T>)
    ensures
        *v == t,
;
