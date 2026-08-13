    pub const fn rchunks_mut(&mut self, chunk_size: usize) -> RChunksMut<'_, T> {
        assert!(chunk_size != 0, "chunk size must be non-zero");
        RChunksMut::new(self, chunk_size)
    }
