    pub const fn chunks_mut(&mut self, chunk_size: usize) -> ChunksMut<'_, T> {
        assert!(chunk_size != 0, "chunk size must be non-zero");
        ChunksMut::new(self, chunk_size)
    }
