    pub const fn chunks(&self, chunk_size: usize) -> Chunks<'_, T> {
        assert!(chunk_size != 0, "chunk size must be non-zero");
        Chunks::new(self, chunk_size)
    }
