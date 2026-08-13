    pub const fn rchunks_exact_mut(&mut self, chunk_size: usize) -> RChunksExactMut<'_, T> {
        assert!(chunk_size != 0, "chunk size must be non-zero");
        RChunksExactMut::new(self, chunk_size)
    }
