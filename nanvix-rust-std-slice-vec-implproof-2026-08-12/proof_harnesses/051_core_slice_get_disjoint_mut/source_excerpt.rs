    pub fn get_disjoint_mut<I, const N: usize>(
        &mut self,
        indices: [I; N],
    ) -> Result<[&mut I::Output; N], GetDisjointMutError>
    where
        I: GetDisjointMutIndex + SliceIndex<Self>,
    {
        get_disjoint_check_valid(&indices, self.len())?;
        // SAFETY: The `get_disjoint_check_valid()` call checked that all indices
        // are disjunct and in bounds.
        unsafe { Ok(self.get_disjoint_unchecked_mut(indices)) }
    }
