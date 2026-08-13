    pub const fn chunks_exact_mut(&mut self, chunk_size: usize) -> ChunksExactMut<'_, T> {
        assert!(chunk_size != 0, "chunk size must be non-zero");
        ChunksExactMut::new(self, chunk_size)
    }
