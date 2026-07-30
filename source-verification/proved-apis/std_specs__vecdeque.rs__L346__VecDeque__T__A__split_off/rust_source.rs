pub fn split_off(&mut self, at: usize) -> Self
    where
        A: Clone,
    {
        let len = self.len;
        assert!(at <= len, "`at` out of bounds");

        let other_len = len - at;
        let mut other = VecDeque::with_capacity_in(other_len, self.allocator().clone());

        let (first_half, second_half) = self.as_slices();
        let first_len = first_half.len();
        let second_len = second_half.len();

        unsafe {
            if at < first_len {
                // `at` lies in the first half.
                let amount_in_first = first_len - at;

                ptr::copy_nonoverlapping(first_half.as_ptr().add(at), other.ptr(), amount_in_first);

                // just take all of the second half.
                ptr::copy_nonoverlapping(
                    second_half.as_ptr(),
                    other.ptr().add(amount_in_first),
                    second_len,
                );
            } else {
                // `at` lies in the second half, need to factor in the elements we skipped
                // in the first half.
                let offset = at - first_len;
                let amount_in_second = second_len - offset;
                ptr::copy_nonoverlapping(
                    second_half.as_ptr().add(offset),
                    other.ptr(),
                    amount_in_second,
                );
            }
        }

        // Cleanup where the ends of the buffers are
        self.len = at;
        other.len = other_len;

        other
    }
