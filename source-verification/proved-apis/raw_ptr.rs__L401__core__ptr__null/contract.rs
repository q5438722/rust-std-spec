pub assume_specification<
    T: core::marker::PointeeSized + core::ptr::Pointee<Metadata = ()>,
>[ core::ptr::null ]() -> (res: *const T)
    ensures
        res == ptr_null::<T>(),
    opens_invariants none
    no_unwind
;
