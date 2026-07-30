pub fn swap(&mut self, i: usize, j: usize) {
        assert!(i < self.len());
        assert!(j < self.len());
        let ri = self.to_physical_idx(i);
        let rj = self.to_physical_idx(j);
        unsafe { ptr::swap(self.ptr().add(ri), self.ptr().add(rj)) }
    }
