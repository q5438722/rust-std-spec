pub const fn as_secs_f64(&self) -> f64 {
        (self.secs as f64) + (self.nanos.as_inner() as f64) / (NANOS_PER_SEC as f64)
    }
