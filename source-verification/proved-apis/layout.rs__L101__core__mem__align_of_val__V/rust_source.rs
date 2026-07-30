pub const fn align_of_val<T: ?Sized>(val: &T) -> usize {
    // SAFETY: val is a reference, so it's a valid raw pointer
    unsafe { intrinsics::align_of_val(val) }
}
