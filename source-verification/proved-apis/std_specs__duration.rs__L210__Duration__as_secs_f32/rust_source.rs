pub const fn as_secs_f32(&self) -> f32 {
        (self.secs as f32) + (self.nanos.as_inner() as f32) / (NANOS_PER_SEC as f32)
    }
