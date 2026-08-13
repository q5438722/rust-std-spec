    pub const unsafe fn split_at_unchecked(&self, mid: usize) -> (&[T], &[T]) {
        // FIXME(const-hack): the const function `from_raw_parts` is used to make this
        // function const; previously the implementation used
        // `(self.get_unchecked(..mid), self.get_unchecked(mid..))`

        let len = self.len();
        let ptr = self.as_ptr();

        assert_unsafe_precondition!(
            check_library_ub,
            "slice::split_at_unchecked requires the index to be within the slice",
            (mid: usize = mid, len: usize = len) => mid <= len,
        );

        // SAFETY: Caller has to check that `0 <= mid <= self.len()`
        unsafe { (from_raw_parts(ptr, mid), from_raw_parts(ptr.add(mid), unchecked_sub(len, mid))) }
    }
