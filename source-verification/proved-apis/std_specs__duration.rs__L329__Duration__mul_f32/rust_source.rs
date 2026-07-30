pub fn mul_f32(self, rhs: f32) -> Duration {
        Duration::from_secs_f32(rhs * self.as_secs_f32())
    }
