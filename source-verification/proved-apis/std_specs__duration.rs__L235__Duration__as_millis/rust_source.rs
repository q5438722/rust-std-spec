pub const fn as_millis(&self) -> u128 {
        self.secs as u128 * MILLIS_PER_SEC as u128
            + (self.nanos.as_inner() / NANOS_PER_MILLI) as u128
    }
