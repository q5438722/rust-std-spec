pub fn copy_within<R: RangeBounds<usize>>(&mut self, src: R, dest: usize)
    where
        T: Copy,
    {
        let Range { start: src_start, end: src_end } = slice::range(src, ..self.len());
        let count = src_end - src_start;
        assert!(dest <= self.len() - count, "dest is out of bounds");
        // SAFETY: the conditions for `ptr::copy` have all been checked above,
        // as have those for `ptr::add`.
        unsafe {
            // Derive both `src_ptr` and `dest_ptr` from the same loan
            let ptr = self.as_mut_ptr();
            let src_ptr = ptr.add(src_start);
            let dest_ptr = ptr.add(dest);
            ptr::copy(src_ptr, dest_ptr, count);
        }
    }
