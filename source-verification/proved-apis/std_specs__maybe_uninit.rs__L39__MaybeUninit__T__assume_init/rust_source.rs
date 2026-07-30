pub const unsafe fn assume_init(self) -> T {
        // SAFETY: the caller must guarantee that `self` is initialized.
        // This also means that `self` must be a `value` variant.
        unsafe {
            intrinsics::assert_inhabited::<T>();
            // We do this via a raw ptr read instead of `ManuallyDrop::into_inner` so that there's
            // no trace of `ManuallyDrop` in Miri's error messages here.
            (&raw const self.value).cast::<T>().read()
        }
    }
