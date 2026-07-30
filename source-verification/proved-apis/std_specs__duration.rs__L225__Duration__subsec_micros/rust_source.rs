pub const fn subsec_micros(&self) -> u32 {
        self.nanos.as_inner() / NANOS_PER_MICRO
    }
