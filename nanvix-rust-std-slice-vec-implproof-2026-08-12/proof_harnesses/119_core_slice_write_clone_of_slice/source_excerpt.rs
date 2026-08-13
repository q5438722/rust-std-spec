    pub fn write_clone_of_slice(&mut self, src: &[T]) -> &mut [T]
    where
        T: Clone,
    {
        // unlike copy_from_slice this does not call clone_from_slice on the slice
        // this is because `MaybeUninit<T: Clone>` does not implement Clone.

        assert_eq!(self.len(), src.len(), "destination and source slices have different lengths");

        // NOTE: We need to explicitly slice them to the same length
        // for bounds checking to be elided, and the optimizer will
        // generate memcpy for simple cases (for example T = u8).
        let len = self.len();
        let src = &src[..len];

        // guard is needed b/c panic might happen during a clone
        let mut guard = Guard { slice: self, initialized: 0 };

        for i in 0..len {
            guard.slice[i].write(src[i].clone());
            guard.initialized += 1;
        }

        super::forget(guard);

        // SAFETY: Valid elements have just been written into `self` so it is initialized
        unsafe { self.assume_init_mut() }
    }
