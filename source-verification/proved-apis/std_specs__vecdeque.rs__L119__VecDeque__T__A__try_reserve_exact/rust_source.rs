pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {
        let new_cap =
            self.len.checked_add(additional).ok_or(TryReserveErrorKind::CapacityOverflow)?;
        let old_cap = self.capacity();

        if new_cap > old_cap {
            self.buf.try_reserve_exact(self.len, additional)?;
            unsafe {
                self.handle_capacity_increase(old_cap);
            }
        }
        Ok(())
    }
