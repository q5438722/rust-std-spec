pub const fn swap<T>(x: &mut T, y: &mut T) {
    // SAFETY: `&mut` guarantees these are typed readable and writable
    // as well as non-overlapping.
    unsafe { intrinsics::typed_swap_nonoverlapping(x, y) }
}
