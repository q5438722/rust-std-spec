pub const fn from_ref<T>(s: &T) -> &[T; 1] {
    // SAFETY: Converting `&T` to `&[T; 1]` is sound.
    unsafe { &*(s as *const T).cast::<[T; 1]>() }
}
