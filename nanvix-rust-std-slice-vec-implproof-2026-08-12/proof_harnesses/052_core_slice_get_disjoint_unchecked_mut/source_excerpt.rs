    pub unsafe fn get_disjoint_unchecked_mut<I, const N: usize>(
        &mut self,
        indices: [I; N],
    ) -> [&mut I::Output; N]
    where
        I: GetDisjointMutIndex + SliceIndex<Self>,
    {
        // NB: This implementation is written as it is because any variation of
        // `indices.map(|i| self.get_unchecked_mut(i))` would make miri unhappy,
        // or generate worse code otherwise. This is also why we need to go
        // through a raw pointer here.
        let slice: *mut [T] = self;
        let mut arr: MaybeUninit<[&mut I::Output; N]> = MaybeUninit::uninit();
        let arr_ptr = arr.as_mut_ptr();

        // SAFETY: We expect `indices` to contain disjunct values that are
        // in bounds of `self`.
        unsafe {
            for i in 0..N {
                let idx = indices.get_unchecked(i).clone();
                arr_ptr.cast::<&mut I::Output>().add(i).write(&mut *slice.get_unchecked_mut(idx));
            }
            arr.assume_init()
        }
    }
