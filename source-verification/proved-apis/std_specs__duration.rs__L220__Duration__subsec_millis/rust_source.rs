pub const fn subsec_millis(&self) -> u32 {
        self.nanos.as_inner() / NANOS_PER_MILLI
    }
