pub const fn null_mut<T: PointeeSized + Thin>() -> *mut T {
    from_raw_parts_mut(without_provenance_mut::<()>(0), ())
}
