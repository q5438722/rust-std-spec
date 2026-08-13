    pub const fn last_chunk_mut<const N: usize>(&mut self) -> Option<&mut [T; N]> {
        // FIXME(const-hack): Without const traits, we need this instead of `get`.
        let Some(index) = self.len().checked_sub(N) else { return None };
        let (_, last) = self.split_at_mut(index);

        // SAFETY: We explicitly check for the correct number of elements,
        //   do not let the reference outlive the slice,
        //   and require exclusive access to the entire slice to mutate the chunk.
        Some(unsafe { &mut *(last.as_mut_ptr().cast_array()) })
    }
