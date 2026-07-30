pub const unsafe fn assume_init_ref(&self) -> &T {
        // SAFETY: the caller must guarantee that `self` is initialized.
        // This also means that `self` must be a `value` variant.
        unsafe {
            intrinsics::assert_inhabited::<T>();
            &*self.as_ptr()
        }
    }
