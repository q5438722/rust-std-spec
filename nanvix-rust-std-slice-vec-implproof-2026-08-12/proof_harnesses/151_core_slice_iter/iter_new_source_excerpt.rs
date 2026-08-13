impl<'a, T> Iter<'a, T> {
    #[inline]
    pub(super) const fn new(slice: &'a [T]) -> Self {
        let len = slice.len();
        let ptr: NonNull<T> = NonNull::from_ref(slice).cast();
        // SAFETY: Similar to `IterMut::new`.
        unsafe {
            let end_or_len =
                if T::IS_ZST { without_provenance(len) } else { ptr.as_ptr().add(len) };

            Self { ptr, end_or_len, _marker: PhantomData }
        }
    }
}
