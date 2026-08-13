// Original Rust 1.96 target and private constructor before valid-index split adaptation.
// Sources: core/src/slice/mod.rs:1242-1245; core/src/slice/iter.rs:1849-1857
pub const fn chunks_exact(&self, chunk_size: usize) -> ChunksExact<'_, T> {
    assert!(chunk_size != 0, "chunk size must be non-zero");
    ChunksExact::new(self, chunk_size)
}

impl<'a, T> ChunksExact<'a, T> {
    #[inline]
    pub(super) const fn new(slice: &'a [T], chunk_size: usize) -> Self {
        let rem = slice.len() % chunk_size;
        let fst_len = slice.len() - rem;
        // SAFETY: 0 <= fst_len <= slice.len() by construction above
        let (fst, snd) = unsafe { slice.split_at_unchecked(fst_len) };
        Self { v: fst, rem: snd, chunk_size }
    }
}
