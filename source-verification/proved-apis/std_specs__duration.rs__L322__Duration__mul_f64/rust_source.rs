pub fn mul_f64(self, rhs: f64) -> Duration {
        Duration::from_secs_f64(rhs * self.as_secs_f64())
    }
