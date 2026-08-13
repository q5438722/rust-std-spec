    pub const fn as_chunks<const N: usize>(&self) -> (&[[T; N]], &[T]) {
        assert!(N != 0, "chunk size must be non-zero");
        let len_rounded_down = self.len() / N * N;
        // SAFETY: The rounded-down value is always the same or smaller than the
        // original length, and thus must be in-bounds of the slice.
        let (multiple_of_n, remainder) = unsafe { self.split_at_unchecked(len_rounded_down) };
        // SAFETY: We already panicked for zero, and ensured by construction
        // that the length of the subslice is a multiple of N.
        let array_slice = unsafe { multiple_of_n.as_chunks_unchecked() };
        (array_slice, remainder)
    }
