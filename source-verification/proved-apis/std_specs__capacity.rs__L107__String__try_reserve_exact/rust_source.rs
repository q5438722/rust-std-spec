pub fn try_reserve_exact(&mut self, additional: usize) -> Result<(), TryReserveError> {
        self.vec.try_reserve_exact(additional)
    }
