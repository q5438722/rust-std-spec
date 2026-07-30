pub assume_specification<T: core::marker::PointeeSized>[ <*const T as PartialEq<*const T>>::eq ](
    x: &*const T,
    y: &*const T,
) -> (res: bool)
    ensures
        res <==> (x@.addr == y@.addr) && (x@.metadata == y@.metadata),
;
