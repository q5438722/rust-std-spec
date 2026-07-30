pub assume_specification<T: ?Sized>[ <ManuallyDrop<T> as Deref>::deref ](
    m: &ManuallyDrop<T>,
) -> (res: &T)
    returns
        m.view_ref(),
;
