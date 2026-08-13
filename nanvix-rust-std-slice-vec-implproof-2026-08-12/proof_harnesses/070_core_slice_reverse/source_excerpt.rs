    pub const fn reverse(&mut self) {
        let half_len = self.len() / 2;
        let Range { start, end } = self.as_mut_ptr_range();

        // These slices will skip the middle item for an odd length,
        // since that one doesn't need to move.
        let (front_half, back_half) =
            // SAFETY: Both are subparts of the original slice, so the memory
            // range is valid, and they don't overlap because they're each only
            // half (or less) of the original slice.
            unsafe {
                (
                    slice::from_raw_parts_mut(start, half_len),
                    slice::from_raw_parts_mut(end.sub(half_len), half_len),
                )
            };

        // Introducing a function boundary here means that the two halves
        // get `noalias` markers, allowing better optimization as LLVM
        // knows that they're disjoint, unlike in the original slice.
        revswap(front_half, back_half, half_len);

        #[inline]
        const fn revswap<T>(a: &mut [T], b: &mut [T], n: usize) {
            debug_assert!(a.len() == n);
            debug_assert!(b.len() == n);

            // Because this function is first compiled in isolation,
            // this check tells LLVM that the indexing below is
            // in-bounds. Then after inlining -- once the actual
            // lengths of the slices are known -- it's removed.
            // FIXME(const_trait_impl) replace with let (a, b) = (&mut a[..n], &mut b[..n]);
            let (a, _) = a.split_at_mut(n);
            let (b, _) = b.split_at_mut(n);

            let mut i = 0;
            while i < n {
                mem::swap(&mut a[i], &mut b[n - 1 - i]);
                i += 1;
            }
        }
    }
