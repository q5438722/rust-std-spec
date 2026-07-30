pub const unsafe fn assume_init_mut(&mut self) -> &mut T {
        // SAFETY: the caller must guarantee that `self` is initialized.
        // This also means that `self` must be a `value` variant.
        unsafe {
            intrinsics::assert_inhabited::<T>();
            &mut *self.as_mut_ptr()
        }
    }
