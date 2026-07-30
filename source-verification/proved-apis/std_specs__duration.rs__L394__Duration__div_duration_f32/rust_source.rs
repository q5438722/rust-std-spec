pub const fn div_duration_f32(self, rhs: Duration) -> f32 {
        let self_nanos =
            (self.secs as f32) * (NANOS_PER_SEC as f32) + (self.nanos.as_inner() as f32);
        let rhs_nanos = (rhs.secs as f32) * (NANOS_PER_SEC as f32) + (rhs.nanos.as_inner() as f32);
        self_nanos / rhs_nanos
    }
