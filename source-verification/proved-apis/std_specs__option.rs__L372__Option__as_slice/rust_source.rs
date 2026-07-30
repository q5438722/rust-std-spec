pub const fn as_slice(&self) -> &[T] {
        // SAFETY: When the `Option` is `Some`, we're using the actual pointer
        // to the payload, with a length of 1, so this is equivalent to
        // `slice::from_ref`, and thus is safe.
        // When the `Option` is `None`, the length used is 0, so to be safe it
        // just needs to be aligned, which it is because `&self` is aligned and
        // the offset used is a multiple of alignment.
        //
        // Here we assume that `offset_of!` always returns an offset to an
        // in-bounds and correctly aligned position for a `T` (even if in the
        // `None` case it's just padding).
        unsafe {
            slice::from_raw_parts(
                (self as *const Self).byte_add(core::mem::offset_of!(Self, Some.0)).cast(),
                self.len(),
            )
        }
    }
