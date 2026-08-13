    pub const fn as_slice(&self) -> &[T] {
        // SAFETY: `slice::from_raw_parts` requires pointee is a contiguous, aligned buffer of size
        // `len` containing properly-initialized `T`s. Data must not be mutated for the returned
        // lifetime. Further, `len * size_of::<T>` <= `isize::MAX`, and allocation does not
        // "wrap" through overflowing memory addresses.
        //
        // * Vec API guarantees that self.buf:
        //      * contains only properly-initialized items within 0..len
        //      * is aligned, contiguous, and valid for `len` reads
        //      * obeys size and address-wrapping constraints
        //
        // * We only construct `&mut` references to `self.buf` through `&mut self` methods; borrow-
        //   check ensures that it is not possible to mutably alias `self.buf` within the
        //   returned lifetime.
        unsafe {
            // normally this would use `slice::from_raw_parts`, but it's
            // instantiated often enough that avoiding the UB check is worth it
            &*core::intrinsics::aggregate_raw_ptr::<*const [T], _, _>(self.as_ptr(), self.len)
        }
    }
