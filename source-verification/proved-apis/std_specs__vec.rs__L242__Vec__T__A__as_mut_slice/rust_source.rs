pub const fn as_mut_slice(&mut self) -> &mut [T] {
        // SAFETY: `slice::from_raw_parts_mut` requires pointee is a contiguous, aligned buffer of
        // size `len` containing properly-initialized `T`s. Data must not be accessed through any
        // other pointer for the returned lifetime. Further, `len * size_of::<T>` <=
        // `isize::MAX` and allocation does not "wrap" through overflowing memory addresses.
        //
        // * Vec API guarantees that self.buf:
        //      * contains only properly-initialized items within 0..len
        //      * is aligned, contiguous, and valid for `len` reads
        //      * obeys size and address-wrapping constraints
        //
        // * We only construct references to `self.buf` through `&self` and `&mut self` methods;
        //   borrow-check ensures that it is not possible to construct a reference to `self.buf`
        //   within the returned lifetime.
        unsafe {
            // normally this would use `slice::from_raw_parts_mut`, but it's
            // instantiated often enough that avoiding the UB check is worth it
            &mut *core::intrinsics::aggregate_raw_ptr::<*mut [T], _, _>(self.as_mut_ptr(), self.len)
        }
    }
