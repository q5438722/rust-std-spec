    pub fn element_offset(&self, element: &T) -> Option<usize> {
        if T::IS_ZST {
            panic!("elements are zero-sized");
        }

        let self_start = self.as_ptr().addr();
        let elem_start = ptr::from_ref(element).addr();

        let byte_offset = elem_start.wrapping_sub(self_start);

        if !byte_offset.is_multiple_of(size_of::<T>()) {
            return None;
        }

        let offset = byte_offset / size_of::<T>();

        if offset < self.len() { Some(offset) } else { None }
    }
