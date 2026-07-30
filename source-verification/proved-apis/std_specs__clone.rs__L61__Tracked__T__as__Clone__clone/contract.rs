pub assume_specification<T: Copy>[ <Tracked<T> as Clone>::clone ](b: &Tracked<T>) -> (res: Tracked<
    T,
>)
    ensures
        res == b,
;
