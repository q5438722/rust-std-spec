pub fn div_f32(self, rhs: f32) -> Duration {
        Duration::from_secs_f32(self.as_secs_f32() / rhs)
    }
