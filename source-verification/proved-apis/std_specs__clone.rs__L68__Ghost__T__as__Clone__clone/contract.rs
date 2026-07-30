pub assume_specification<T>[ <Ghost<T> as Clone>::clone ](b: &Ghost<T>) -> (res: Ghost<T>)
    ensures
        res == b,
;
