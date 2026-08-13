    pub const fn eq_ignore_ascii_case(&self, other: &[u8]) -> bool {
        if self.len() != other.len() {
            return false;
        }

        #[cfg(all(target_arch = "x86_64", target_feature = "sse2"))]
        {
            const CHUNK_SIZE: usize = 16;
            // The following function has two invariants:
            // 1. The slice lengths must be equal, which we checked above.
            // 2. The slice lengths must greater than or equal to N, which this
            //    if-statement is checking.
            if self.len() >= CHUNK_SIZE {
                return self.eq_ignore_ascii_case_chunks::<CHUNK_SIZE>(other);
            }
        }

        self.eq_ignore_ascii_case_simple(other)
    }
