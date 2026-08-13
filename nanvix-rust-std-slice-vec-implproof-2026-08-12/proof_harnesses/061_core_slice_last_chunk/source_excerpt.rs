    pub const fn last_chunk<const N: usize>(&self) -> Option<&[T; N]> {
        // FIXME(const-hack): Without const traits, we need this instead of `get`.
        let Some(index) = self.len().checked_sub(N) else { return None };
        let (_, last) = self.split_at(index);

        // SAFETY: We explicitly check for the correct number of elements,
        //   and do not let the references outlive the slice.
        Some(unsafe { &*(last.as_ptr().cast_array()) })
    }
