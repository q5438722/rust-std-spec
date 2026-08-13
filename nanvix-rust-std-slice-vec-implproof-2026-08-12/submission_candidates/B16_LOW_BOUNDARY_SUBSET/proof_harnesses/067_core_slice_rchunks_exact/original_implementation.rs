// Original Rust 1.96 target and private constructor before valid-index split adaptation.
// Sources: core/src/slice/mod.rs:1775-1778; core/src/slice/iter.rs:2659-2666
pub const fn rchunks_exact(&self, chunk_size: usize) -> RChunksExact<'_, T> {
    assert!(chunk_size != 0, "chunk size must be non-zero");
    RChunksExact::new(self, chunk_size)
}

impl<'a, T> RChunksExact<'a, T> {
    #[inline]
    pub(super) const fn new(slice: &'a [T], chunk_size: usize) -> Self {
        let rem = slice.len() % chunk_size;
        // SAFETY: 0 <= rem <= slice.len() by construction above
        let (fst, snd) = unsafe { slice.split_at_unchecked(rem) };
        Self { v: snd, rem: fst, chunk_size }
    }
}
