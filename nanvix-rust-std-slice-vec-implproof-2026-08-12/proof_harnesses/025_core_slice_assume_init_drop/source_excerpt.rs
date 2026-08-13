    pub const unsafe fn assume_init_drop(&mut self)
    where
        T: [const] Destruct,
    {
        if !self.is_empty() {
            // SAFETY: the caller must guarantee that every element of `self`
            // is initialized and satisfies all invariants of `T`.
            // Dropping the value in place is safe if that is the case.
            unsafe { ptr::drop_in_place(self as *mut [MaybeUninit<T>] as *mut [T]) }
        }
    }
