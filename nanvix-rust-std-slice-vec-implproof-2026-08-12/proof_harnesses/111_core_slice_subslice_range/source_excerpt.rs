    pub fn subslice_range(&self, subslice: &[T]) -> Option<core::range::Range<usize>> {
        if T::IS_ZST {
            panic!("elements are zero-sized");
        }

        let self_start = self.as_ptr().addr();
        let subslice_start = subslice.as_ptr().addr();

        let byte_start = subslice_start.wrapping_sub(self_start);

        if !byte_start.is_multiple_of(size_of::<T>()) {
            return None;
        }

        let start = byte_start / size_of::<T>();
        let end = start.wrapping_add(subslice.len());

        if start <= self.len() && end <= self.len() {
            Some(core::range::Range { start, end })
        } else {
            None
        }
    }
