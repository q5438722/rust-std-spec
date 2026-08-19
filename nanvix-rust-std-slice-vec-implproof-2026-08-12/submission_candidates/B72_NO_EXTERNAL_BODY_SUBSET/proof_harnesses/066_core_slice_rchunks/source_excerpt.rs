    pub const fn rchunks(&self, chunk_size: usize) -> RChunks<'_, T> {
        assert!(chunk_size != 0, "chunk size must be non-zero");
        RChunks::new(self, chunk_size)
    }
