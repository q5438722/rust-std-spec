pub assume_specification<T: Clone + ?Sized>[ <ManuallyDrop<T> as Clone>::clone ](
    m: &ManuallyDrop<T>,
) -> (res: ManuallyDrop<T>)
    ensures
        cloned(m@, res@),
;
