pub fn clear(&mut self) {
        let elems: *mut [T] = self.as_mut_slice();

        // SAFETY:
        // - `elems` comes directly from `as_mut_slice` and is therefore valid.
        // - Setting `self.len` before calling `drop_in_place` means that,
        //   if an element's `Drop` impl panics, the vector's `Drop` impl will
        //   do nothing (leaking the rest of the elements) instead of dropping
        //   some twice.
        unsafe {
            self.len = 0;
            ptr::drop_in_place(elems);
        }
    }
