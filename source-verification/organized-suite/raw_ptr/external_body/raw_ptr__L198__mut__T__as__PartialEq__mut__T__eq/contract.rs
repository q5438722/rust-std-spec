pub assume_specification<T: core::marker::PointeeSized>[ <*mut T as PartialEq<*mut T>>::eq ](
    x: &*mut T,
    y: &*mut T,
) -> (res: bool)
    ensures
        res <==> (x@.addr == y@.addr) && (x@.metadata == y@.metadata),
;
