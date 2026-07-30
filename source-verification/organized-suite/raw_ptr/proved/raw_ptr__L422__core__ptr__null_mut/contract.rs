pub assume_specification<
    T: core::marker::PointeeSized + core::ptr::Pointee<Metadata = ()>,
>[ core::ptr::null_mut ]() -> (res: *mut T)
    ensures
        res == ptr_null_mut::<T>(),
    opens_invariants none
    no_unwind
;
