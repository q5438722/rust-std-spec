    pub const fn split_last_chunk<const N: usize>(&self) -> Option<(&[T], &[T; N])> {
        let Some(index) = self.len().checked_sub(N) else { return None };
        let (init, last) = self.split_at(index);

        // SAFETY: We explicitly check for the correct number of elements,
        //   and do not let the references outlive the slice.
        Some((init, unsafe { &*(last.as_ptr().cast_array()) }))
    }
