    /// The first will contain all indices from `[0, mid)` (excluding
    /// the index `mid` itself) and the second will contain all
    /// indices from `[mid, len)` (excluding the index `len` itself).
    ///
    /// # Panics
    ///
    /// Panics if `mid > len`.  For a non-panicking alternative see
    /// [`split_at_mut_checked`](slice::split_at_mut_checked).
    ///
    /// # Examples
    ///
    /// ```
    /// let mut v = [1, 0, 3, 0, 5, 6];
    /// let (left, right) = v.split_at_mut(2);
    /// assert_eq!(left, [1, 0]);
    /// assert_eq!(right, [3, 0, 5, 6]);
    /// left[1] = 2;
    /// right[1] = 4;
    /// assert_eq!(v, [1, 2, 3, 4, 5, 6]);
    /// ```
    #[stable(feature = "rust1", since = "1.0.0")]
    #[inline]
    #[track_caller]
    #[must_use]
    #[rustc_const_stable(feature = "const_slice_split_at_mut", since = "1.83.0")]
    pub const fn split_at_mut(&mut self, mid: usize) -> (&mut [T], &mut [T]) {
        match self.split_at_mut_checked(mid) {
            Some(pair) => pair,
            None => panic!("mid > len"),
        }
    }
