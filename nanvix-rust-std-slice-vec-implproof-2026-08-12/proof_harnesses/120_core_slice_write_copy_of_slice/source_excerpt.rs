    pub const fn write_copy_of_slice(&mut self, src: &[T]) -> &mut [T]
    where
        T: Copy,
    {
        // SAFETY: &[T] and &[MaybeUninit<T>] have the same layout
        let uninit_src: &[MaybeUninit<T>] = unsafe { super::transmute(src) };

        self.copy_from_slice(uninit_src);

        // SAFETY: Valid elements have just been copied into `self` so it is initialized
        unsafe { self.assume_init_mut() }
    }
