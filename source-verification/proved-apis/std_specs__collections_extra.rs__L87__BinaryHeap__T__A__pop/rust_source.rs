pub fn pop(&mut self) -> Option<T> {
        self.data.pop().map(|mut item| {
            if !self.is_empty() {
                swap(&mut item, &mut self.data[0]);
                // SAFETY: !self.is_empty() means that self.len() > 0
                unsafe { self.sift_down_to_bottom(0) };
            }
            item
        })
    }
