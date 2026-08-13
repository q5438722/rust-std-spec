    pub const fn as_flattened_mut(&mut self) -> &mut [T] {
        let len = if T::IS_ZST {
            self.len().checked_mul(N).expect("slice len overflow")
        } else {
            // SAFETY: `self.len() * N` cannot overflow because `self` is
            // already in the address space.
            unsafe { self.len().unchecked_mul(N) }
        };
        // SAFETY: `[T]` is layout-identical to `[T; N]`
        unsafe { from_raw_parts_mut(self.as_mut_ptr().cast(), len) }
    }
