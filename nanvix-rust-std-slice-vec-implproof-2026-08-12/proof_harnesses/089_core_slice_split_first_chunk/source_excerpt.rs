    pub const fn split_first_chunk<const N: usize>(&self) -> Option<(&[T; N], &[T])> {
        let Some((first, tail)) = self.split_at_checked(N) else { return None };

        // SAFETY: We explicitly check for the correct number of elements,
        //   and do not let the references outlive the slice.
        Some((unsafe { &*(first.as_ptr().cast_array()) }, tail))
    }
