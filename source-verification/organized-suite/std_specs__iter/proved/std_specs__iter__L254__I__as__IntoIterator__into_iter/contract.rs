pub assume_specification<I: Iterator>[ <I as IntoIterator>::into_iter ](i: I) -> (r: I)
    ensures
        r == i,
;
