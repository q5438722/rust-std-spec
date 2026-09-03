    pub const unsafe fn as_chunks_unchecked_mut<const N: usize>(&mut self) -> &mut [[T; N]] {
        assert_unsafe_precondition!(
            check_language_ub,
            "slice::as_chunks_unchecked requires `N != 0` and the slice to split exactly into `N`-element chunks",
            (n: usize = N, len: usize = self.len()) => n != 0 && len.is_multiple_of(n)
        );
        // SAFETY: Caller must guarantee that `N` is nonzero and exactly divides the slice length
        let new_len = unsafe { exact_div(self.len(), N) };
        // SAFETY: We cast a slice of `new_len * N` elements into
        // a slice of `new_len` many `N` elements chunks.
        unsafe { from_raw_parts_mut(self.as_mut_ptr().cast(), new_len) }
    }
