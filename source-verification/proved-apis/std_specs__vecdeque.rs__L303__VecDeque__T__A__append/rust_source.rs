pub fn append(&mut self, other: &mut Self) {
        if T::IS_ZST {
            self.len = self.len.checked_add(other.len).expect("capacity overflow");
            other.len = 0;
            other.head = 0;
            return;
        }

        self.reserve(other.len);
        unsafe {
            let (left, right) = other.as_slices();
            self.copy_slice(self.to_physical_idx(self.len), left);
            // no overflow, because self.capacity() >= old_cap + left.len() >= self.len + left.len()
            self.copy_slice(self.to_physical_idx(self.len + left.len()), right);
        }
        // SAFETY: Update pointers after copying to avoid leaving doppelganger
        // in case of panics.
        self.len += other.len;
        // Now that we own its values, forget everything in `other`.
        other.len = 0;
        other.head = 0;
    }
