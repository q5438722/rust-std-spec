pub fn get(&self, index: usize) -> Option<&T> {
        if index < self.len {
            let idx = self.to_physical_idx(index);
            unsafe { Some(&*self.ptr().add(idx)) }
        } else {
            None
        }
    }
