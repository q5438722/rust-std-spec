    pub const unsafe fn assume_init_ref(&self) -> &[T] {
        // SAFETY: casting `slice` to a `*const [T]` is safe since the caller guarantees that
        // `slice` is initialized, and `MaybeUninit` is guaranteed to have the same layout as `T`.
        // The pointer obtained is valid since it refers to memory owned by `slice` which is a
        // reference and thus guaranteed to be valid for reads.
        unsafe { &*(self as *const Self as *const [T]) }
    }
