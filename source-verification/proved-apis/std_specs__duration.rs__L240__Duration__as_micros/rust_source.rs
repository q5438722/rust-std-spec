pub const fn as_micros(&self) -> u128 {
        self.secs as u128 * MICROS_PER_SEC as u128
            + (self.nanos.as_inner() / NANOS_PER_MICRO) as u128
    }
