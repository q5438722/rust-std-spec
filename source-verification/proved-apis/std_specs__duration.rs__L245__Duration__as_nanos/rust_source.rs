pub const fn as_nanos(&self) -> u128 {
        self.secs as u128 * NANOS_PER_SEC as u128 + self.nanos.as_inner() as u128
    }
