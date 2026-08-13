impl<'a, T> IterMut<'a, T> {
    #[inline]
    pub(super) const fn new(slice: &'a mut [T]) -> Self {
        let len = slice.len();
        let ptr: NonNull<T> = NonNull::from_mut(slice).cast();
        // SAFETY: There are several things here:
        //
        // `ptr` has been obtained by `slice.as_ptr()` where `slice` is a valid
        // reference thus it is non-NUL and safe to use and pass to
        // `NonNull::new_unchecked` .
        //
        // Adding `slice.len()` to the starting pointer gives a pointer
        // at the end of `slice`. `end` will never be dereferenced, only checked
        // for direct pointer equality with `ptr` to check if the iterator is
        // done.
        //
        // In the case of a ZST, the end pointer is just the length.  It's never
        // used as a pointer at all, and thus it's fine to have no provenance.
        //
        // See the `next_unchecked!` and `is_empty!` macros as well as the
        // `post_inc_start` method for more information.
        unsafe {
            let end_or_len =
                if T::IS_ZST { without_provenance_mut(len) } else { ptr.as_ptr().add(len) };

            Self { ptr, end_or_len, _marker: PhantomData }
        }
    }
}
