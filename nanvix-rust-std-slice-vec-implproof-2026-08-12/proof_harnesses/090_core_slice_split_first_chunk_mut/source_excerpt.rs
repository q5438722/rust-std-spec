    pub const fn split_first_chunk_mut<const N: usize>(
        &mut self,
    ) -> Option<(&mut [T; N], &mut [T])> {
        let Some((first, tail)) = self.split_at_mut_checked(N) else { return None };

        // SAFETY: We explicitly check for the correct number of elements,
        //   do not let the reference outlive the slice,
        //   and enforce exclusive mutability of the chunk by the split.
        Some((unsafe { &mut *(first.as_mut_ptr().cast_array()) }, tail))
    }
