pub const fn abs_diff(self, other: Duration) -> Duration {
        if let Some(res) = self.checked_sub(other) { res } else { other.checked_sub(self).unwrap() }
    }
