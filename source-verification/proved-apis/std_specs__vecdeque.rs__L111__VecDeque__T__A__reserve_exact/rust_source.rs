pub fn reserve_exact(&mut self, additional: usize) {
        let new_cap = self.len.checked_add(additional).expect("capacity overflow");
        let old_cap = self.capacity();

        if new_cap > old_cap {
            self.buf.reserve_exact(self.len, additional);
            unsafe {
                self.handle_capacity_increase(old_cap);
            }
        }
    }
