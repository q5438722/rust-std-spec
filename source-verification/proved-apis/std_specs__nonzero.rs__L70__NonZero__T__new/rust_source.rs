pub const fn new(n: T) -> Option<Self> {
        // SAFETY: Memory layout optimization guarantees that `Option<NonZero<T>>` has
        //         the same layout and size as `T`, with `0` representing `None`.
        unsafe { intrinsics::transmute_unchecked(n) }
    }
