pub const fn null<T: PointeeSized + Thin>() -> *const T {
    from_raw_parts(without_provenance::<()>(0), ())
}
