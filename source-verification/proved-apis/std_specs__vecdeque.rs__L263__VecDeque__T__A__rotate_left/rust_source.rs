pub fn rotate_left(&mut self, n: usize) {
        assert!(n <= self.len());
        let k = self.len - n;
        if n <= k {
            unsafe { self.rotate_left_inner(n) }
        } else {
            unsafe { self.rotate_right_inner(k) }
        }
    }
