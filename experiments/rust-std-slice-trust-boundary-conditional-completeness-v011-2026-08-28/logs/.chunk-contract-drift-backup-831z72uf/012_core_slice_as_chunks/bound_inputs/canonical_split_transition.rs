    /// Divides one slice into two at an index, without doing bounds checking.
    ///
    /// The first will contain all indices from `[0, mid)` (excluding
    /// the index `mid` itself) and the second will contain all
    /// indices from `[mid, len)` (excluding the index `len` itself).
    ///
    /// For a safe alternative see [`split_at`].
    ///
    /// # Safety
    ///
    /// Calling this method with an out-of-bounds index is *[undefined behavior]*
    /// even if the resulting reference is not used. The caller has to ensure that
    /// `0 <= mid <= self.len()`.
    ///
    /// [`split_at`]: slice::split_at
    /// [undefined behavior]: https://doc.rust-lang.org/reference/behavior-considered-undefined.html
    ///
    /// # Examples
    ///
    /// ```
    /// let v = ['a', 'b', 'c'];
    ///
    /// unsafe {
    ///    let (left, right) = v.split_at_unchecked(0);
    ///    assert_eq!(left, []);
    ///    assert_eq!(right, ['a', 'b', 'c']);
    /// }
    ///
    /// unsafe {
    ///     let (left, right) = v.split_at_unchecked(2);
    ///     assert_eq!(left, ['a', 'b']);
    ///     assert_eq!(right, ['c']);
    /// }
    ///
    /// unsafe {
    ///     let (left, right) = v.split_at_unchecked(3);
    ///     assert_eq!(left, ['a', 'b', 'c']);
    ///     assert_eq!(right, []);
    /// }
    /// ```
    #[stable(feature = "slice_split_at_unchecked", since = "1.79.0")]
    #[rustc_const_stable(feature = "const_slice_split_at_unchecked", since = "1.77.0")]
    #[inline]
    #[must_use]
    #[track_caller]
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
