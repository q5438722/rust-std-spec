    pub const fn chunks_exact(&self, chunk_size: usize) -> ChunksExact<'_, T> {
        assert!(chunk_size != 0, "chunk size must be non-zero");
        ChunksExact::new(self, chunk_size)
    }
