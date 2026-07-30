pub const fn len(&self) -> usize {
        ptr::metadata(self)
    }
