    pub const fn rchunks_exact(&self, chunk_size: usize) -> RChunksExact<'_, T> {
        assert!(chunk_size != 0, "chunk size must be non-zero");
        RChunksExact::new(self, chunk_size)
    }
