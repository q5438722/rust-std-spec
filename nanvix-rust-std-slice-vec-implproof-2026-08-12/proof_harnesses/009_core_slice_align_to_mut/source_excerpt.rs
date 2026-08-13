    pub unsafe fn align_to_mut<U>(&mut self) -> (&mut [T], &mut [U], &mut [T]) {
        // Note that most of this function will be constant-evaluated,
        if U::IS_ZST || T::IS_ZST {
            // handle ZSTs specially, which is – don't handle them at all.
            return (self, &mut [], &mut []);
        }

        // First, find at what point do we split between the first and 2nd slice. Easy with
        // ptr.align_offset.
        let ptr = self.as_ptr();
        // SAFETY: Here we are ensuring we will use aligned pointers for U for the
        // rest of the method. This is done by passing a pointer to &[T] with an
        // alignment targeted for U.
        // `crate::ptr::align_offset` is called with a correctly aligned and
        // valid pointer `ptr` (it comes from a reference to `self`) and with
        // a size that is a power of two (since it comes from the alignment for U),
        // satisfying its safety constraints.
        let offset = unsafe { crate::ptr::align_offset(ptr, align_of::<U>()) };
        if offset > self.len() {
            (self, &mut [], &mut [])
        } else {
            let (left, rest) = self.split_at_mut(offset);
            let (us_len, ts_len) = rest.align_to_offsets::<U>();
            let rest_len = rest.len();
            let mut_ptr = rest.as_mut_ptr();
            // Inform Miri that we want to consider the "middle" pointer to be suitably aligned.
            #[cfg(miri)]
            crate::intrinsics::miri_promise_symbolic_alignment(
                mut_ptr.cast() as *const (),
                align_of::<U>(),
            );
            // We can't use `rest` again after this, that would invalidate its alias `mut_ptr`!
            // SAFETY: see comments for `align_to`.
            unsafe {
                (
                    left,
                    from_raw_parts_mut(mut_ptr as *mut U, us_len),
                    from_raw_parts_mut(mut_ptr.add(rest_len - ts_len), ts_len),
                )
            }
        }
    }
