    pub fn retain_mut<F>(&mut self, mut f: F)
    where
        F: FnMut(&mut T) -> bool,
    {
        let original_len = self.len();

        if original_len == 0 {
            // Empty case: explicit return allows better optimization, vs letting compiler infer it
            return;
        }

        // Vec: [Kept, Kept, Hole, Hole, Hole, Hole, Unchecked, Unchecked]
        //      |            ^- write                ^- read             |
        //      |<-              original_len                          ->|
        // Kept: Elements which predicate returns true on.
        // Hole: Moved or dropped element slot.
        // Unchecked: Unchecked valid elements.
        //
        // This drop guard will be invoked when predicate or `drop` of element panicked.
        // It shifts unchecked elements to cover holes and `set_len` to the correct length.
        // In cases when predicate and `drop` never panick, it will be optimized out.
        struct PanicGuard<'a, T, A: Allocator> {
            v: &'a mut Vec<T, A>,
            read: usize,
            write: usize,
            original_len: usize,
        }

        impl<T, A: Allocator> Drop for PanicGuard<'_, T, A> {
            #[cold]
            fn drop(&mut self) {
                let remaining = self.original_len - self.read;
                // SAFETY: Trailing unchecked items must be valid since we never touch them.
                unsafe {
                    ptr::copy(
                        self.v.as_ptr().add(self.read),
                        self.v.as_mut_ptr().add(self.write),
                        remaining,
                    );
                }
                // SAFETY: After filling holes, all items are in contiguous memory.
                unsafe {
                    self.v.set_len(self.write + remaining);
                }
            }
        }

        let mut read = 0;
        loop {
            // SAFETY: read < original_len
            let cur = unsafe { self.get_unchecked_mut(read) };
            if hint::unlikely(!f(cur)) {
                break;
            }
            read += 1;
            if read == original_len {
                // All elements are kept, return early.
                return;
            }
        }

        // Critical section starts here and at least one element is going to be removed.
        // Advance `g.read` early to avoid double drop if `drop_in_place` panicked.
        let mut g = PanicGuard { v: self, read: read + 1, write: read, original_len };
        // SAFETY: previous `read` is always less than original_len.
        unsafe { ptr::drop_in_place(&mut *g.v.as_mut_ptr().add(read)) };

        while g.read < g.original_len {
            // SAFETY: `read` is always less than original_len.
            let cur = unsafe { &mut *g.v.as_mut_ptr().add(g.read) };
            if !f(cur) {
                // Advance `read` early to avoid double drop if `drop_in_place` panicked.
                g.read += 1;
                // SAFETY: We never touch this element again after dropped.
                unsafe { ptr::drop_in_place(cur) };
            } else {
                // SAFETY: `read` > `write`, so the slots don't overlap.
                // We use copy for move, and never touch the source element again.
                unsafe {
                    let hole = g.v.as_mut_ptr().add(g.write);
                    ptr::copy_nonoverlapping(cur, hole, 1);
                }
                g.write += 1;
                g.read += 1;
            }
        }

        // We are leaving the critical section and no panic happened,
        // Commit the length change and forget the guard.
        // SAFETY: `write` is always less than or equal to original_len.
        unsafe { g.v.set_len(g.write) };
        mem::forget(g);
    }
