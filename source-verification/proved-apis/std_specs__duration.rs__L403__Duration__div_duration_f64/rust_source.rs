pub const fn div_duration_f64(self, rhs: Duration) -> f64 {
        let self_nanos =
            (self.secs as f64) * (NANOS_PER_SEC as f64) + (self.nanos.as_inner() as f64);
        let rhs_nanos = (rhs.secs as f64) * (NANOS_PER_SEC as f64) + (rhs.nanos.as_inner() as f64);
        self_nanos / rhs_nanos
    }
