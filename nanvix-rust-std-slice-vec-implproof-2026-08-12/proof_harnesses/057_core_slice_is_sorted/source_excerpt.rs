    pub fn is_sorted(&self) -> bool
    where
        T: PartialOrd,
    {
        // This odd number works the best. 32 + 1 extra due to overlapping chunk boundaries.
        const CHUNK_SIZE: usize = 33;
        if self.len() < CHUNK_SIZE {
            return self.windows(2).all(|w| w[0] <= w[1]);
        }
        let mut i = 0;
        // Check in chunks for autovectorization.
        while i < self.len() - CHUNK_SIZE {
            let chunk = &self[i..i + CHUNK_SIZE];
            if !chunk.windows(2).fold(true, |acc, w| acc & (w[0] <= w[1])) {
                return false;
            }
            // We need to ensure that chunk boundaries are also sorted.
            // Overlap the next chunk with the last element of our last chunk.
            i += CHUNK_SIZE - 1;
        }
        self[i..].windows(2).all(|w| w[0] <= w[1])
    }
