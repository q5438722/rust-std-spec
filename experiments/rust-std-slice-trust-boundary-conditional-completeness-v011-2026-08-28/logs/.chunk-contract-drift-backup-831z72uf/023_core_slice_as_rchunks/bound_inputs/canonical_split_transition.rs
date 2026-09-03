
    /// Divides one slice into two at an index.
    ///
    /// The first will contain all indices from `[0, mid)` (excluding
    /// the index `mid` itself) and the second will contain all
    /// indices from `[mid, len)` (excluding the index `len` itself).
    ///
    /// # Panics
    ///
    /// Panics if `mid > len`.  For a non-panicking alternative see
    /// [`split_at_checked`](slice::split_at_checked).
    ///
    /// # Examples
    ///
    /// ```
    /// let v = ['a', 'b', 'c'];
    ///
    /// {
    ///    let (left, right) = v.split_at(0);
    ///    assert_eq!(left, []);
    ///    assert_eq!(right, ['a', 'b', 'c']);
    /// }
    ///
    /// {
    ///     let (left, right) = v.split_at(2);
    ///     assert_eq!(left, ['a', 'b']);
    ///     assert_eq!(right, ['c']);
    /// }
    ///
    /// {
    ///     let (left, right) = v.split_at(3);
    ///     assert_eq!(left, ['a', 'b', 'c']);
    ///     assert_eq!(right, []);
    /// }
    /// ```
    #[stable(feature = "rust1", since = "1.0.0")]
    #[rustc_const_stable(feature = "const_slice_split_at_not_mut", since = "1.71.0")]
    #[inline]
    #[track_caller]
    #[must_use]
    pub const fn split_at(&self, mid: usize) -> (&[T], &[T]) {
        match self.split_at_checked(mid) {
            Some(pair) => pair,
            None => panic!("mid > len"),
        }
    }

    /// Divides one mutable slice into two at an index.
