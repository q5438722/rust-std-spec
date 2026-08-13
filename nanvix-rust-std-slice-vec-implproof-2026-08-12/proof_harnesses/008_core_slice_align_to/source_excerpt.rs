    pub unsafe fn align_to<U>(&self) -> (&[T], &[U], &[T]) {
        // Note that most of this function will be constant-evaluated,
        if U::IS_ZST || T::IS_ZST {
            // handle ZSTs specially, which is – don't handle them at all.
            return (self, &[], &[]);
        }

        // First, find at what point do we split between the first and 2nd slice. Easy with
        // ptr.align_offset.
        let ptr = self.as_ptr();
        // SAFETY: See the `align_to_mut` method for the detailed safety comment.
        let offset = unsafe { crate::ptr::align_offset(ptr, align_of::<U>()) };
        if offset > self.len() {
            (self, &[], &[])
        } else {
            let (left, rest) = self.split_at(offset);
            let (us_len, ts_len) = rest.align_to_offsets::<U>();
            // Inform Miri that we want to consider the "middle" pointer to be suitably aligned.
            #[cfg(miri)]
            crate::intrinsics::miri_promise_symbolic_alignment(
                rest.as_ptr().cast(),
                align_of::<U>(),
            );
            // SAFETY: now `rest` is definitely aligned, so `from_raw_parts` below is okay,
            // since the caller guarantees that we can transmute `T` to `U` safely.
            unsafe {
                (
                    left,
                    from_raw_parts(rest.as_ptr() as *const U, us_len),
                    from_raw_parts(rest.as_ptr().add(rest.len() - ts_len), ts_len),
                )
            }
        }
    }
