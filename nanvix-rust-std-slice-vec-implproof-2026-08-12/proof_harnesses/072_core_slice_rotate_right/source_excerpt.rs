    pub const fn rotate_right(&mut self, k: usize) {
        assert!(k <= self.len());
        let mid = self.len() - k;
        let p = self.as_mut_ptr();

        // SAFETY: The range `[p.add(mid) - mid, p.add(mid) + k)` is trivially
        // valid for reading and writing, as required by `ptr_rotate`.
        unsafe {
            rotate::ptr_rotate(mid, p.add(mid), k);
        }
    }
