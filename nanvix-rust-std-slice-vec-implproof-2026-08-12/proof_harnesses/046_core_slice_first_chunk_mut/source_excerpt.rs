    pub const fn first_chunk_mut<const N: usize>(&mut self) -> Option<&mut [T; N]> {
        if self.len() < N {
            None
        } else {
            // SAFETY: We explicitly check for the correct number of elements,
            //   do not let the reference outlive the slice,
            //   and require exclusive access to the entire slice to mutate the chunk.
            Some(unsafe { &mut *(self.as_mut_ptr().cast_array()) })
        }
    }
