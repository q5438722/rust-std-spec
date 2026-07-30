pub fn pop_front(&mut self) -> Option<T> {
        if self.is_empty() {
            None
        } else {
            let old_head = self.head;
            self.head = self.to_physical_idx(1);
            self.len -= 1;
            unsafe {
                core::hint::assert_unchecked(self.len < self.capacity());
                Some(self.buffer_read(old_head))
            }
        }
    }
