    pub fn insert_mut(&mut self, index: usize, element: T) -> &mut T {
        #[cold]
        #[cfg_attr(not(panic = "immediate-abort"), inline(never))]
        #[track_caller]
        #[optimize(size)]
        fn assert_failed(index: usize, len: usize) -> ! {
            panic!("insertion index (is {index}) should be <= len (is {len})");
        }

        let len = self.len();
        if index > len {
            assert_failed(index, len);
        }

        // space for the new element
        if len == self.buf.capacity() {
            self.buf.grow_one();
        }

        unsafe {
            // infallible
            // The spot to put the new value
            let p = self.as_mut_ptr().add(index);
            {
                if index < len {
                    // Shift everything over to make space. (Duplicating the
                    // `index`th element into two consecutive places.)
                    ptr::copy(p, p.add(1), len - index);
                }
                // Write it in, overwriting the first copy of the `index`th
                // element.
                ptr::write(p, element);
            }
            self.set_len(len + 1);
            &mut *p
        }
    }
