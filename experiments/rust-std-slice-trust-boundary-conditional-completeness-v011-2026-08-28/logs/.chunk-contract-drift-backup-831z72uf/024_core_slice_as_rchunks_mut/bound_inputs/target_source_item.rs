    pub const fn as_rchunks_mut<const N: usize>(&mut self) -> (&mut [T], &mut [[T; N]]) {
        assert!(N != 0, "chunk size must be non-zero");
        let len = self.len() / N;
        let (remainder, multiple_of_n) = self.split_at_mut(self.len() - len * N);
        // SAFETY: We already panicked for zero, and ensured by construction
        // that the length of the subslice is a multiple of N.
        let array_slice = unsafe { multiple_of_n.as_chunks_unchecked_mut() };
        (remainder, array_slice)
    }
