pub fn shrink_to_fit(&mut self) {
        // The capacity is never less than the length, and there's nothing to do when
        // they are equal, so we can avoid the panic case in `RawVec::shrink_to_fit`
        // by only calling it with a greater capacity.
        if self.capacity() > self.len {
            self.buf.shrink_to_fit(self.len);
        }
    }
