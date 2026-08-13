    pub const fn chunk_by<F>(&self, pred: F) -> ChunkBy<'_, T, F>
    where
        F: FnMut(&T, &T) -> bool,
    {
        ChunkBy::new(self, pred)
    }
