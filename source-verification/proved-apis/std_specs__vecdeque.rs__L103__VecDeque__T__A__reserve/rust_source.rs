pub fn reserve(&mut self, additional: usize) {
        let new_cap = self.len.checked_add(additional).expect("capacity overflow");
        let old_cap = self.capacity();

        if new_cap > old_cap {
            // we don't need to reserve_exact(), as the size doesn't have
            // to be a power of 2.
            self.buf.reserve(self.len, additional);
            unsafe {
                self.handle_capacity_increase(old_cap);
            }
        }
    }
