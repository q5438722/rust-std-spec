pub fn resize(&mut self, new_len: usize, value: T) {
        if new_len > self.len() {
            let extra = new_len - self.len();
            self.extend(repeat_n(value, extra))
        } else {
            self.truncate(new_len);
        }
    }
