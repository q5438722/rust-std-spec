pub const fn from_mut<T>(s: &mut T) -> &mut [T; 1] {
    // SAFETY: Converting `&mut T` to `&mut [T; 1]` is sound.
    unsafe { &mut *(s as *mut T).cast::<[T; 1]>() }
}
