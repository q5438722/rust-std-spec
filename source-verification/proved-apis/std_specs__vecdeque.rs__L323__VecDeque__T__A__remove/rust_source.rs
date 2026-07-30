pub fn remove(&mut self, index: usize) -> Option<T> {
        if self.len <= index {
            return None;
        }

        let wrapped_idx = self.to_physical_idx(index);

        let elem = unsafe { Some(self.buffer_read(wrapped_idx)) };

        let k = self.len - index - 1;
        // safety: due to the nature of the if-condition, whichever wrap_copy gets called,
        // its length argument will be at most `self.len / 2`, so there can't be more than
        // one overlapping area.
        if k < index {
            unsafe { self.wrap_copy(self.wrap_add(wrapped_idx, 1), wrapped_idx, k) };
            self.len -= 1;
        } else {
            let old_head = self.head;
            self.head = self.to_physical_idx(1);
            unsafe { self.wrap_copy(old_head, self.head, index) };
            self.len -= 1;
        }

        elem
    }
