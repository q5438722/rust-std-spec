    pub const fn split_last_chunk_mut<const N: usize>(
        &mut self,
    ) -> Option<(&mut [T], &mut [T; N])> {
        let Some(index) = self.len().checked_sub(N) else { return None };
        let (init, last) = self.split_at_mut(index);

        // SAFETY: We explicitly check for the correct number of elements,
        //   do not let the reference outlive the slice,
        //   and enforce exclusive mutability of the chunk by the split.
        Some((init, unsafe { &mut *(last.as_mut_ptr().cast_array()) }))
    }
