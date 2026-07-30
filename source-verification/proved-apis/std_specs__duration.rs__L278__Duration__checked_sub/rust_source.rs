pub const fn checked_sub(self, rhs: Duration) -> Option<Duration> {
        if let Some(mut secs) = self.secs.checked_sub(rhs.secs) {
            let nanos = if self.nanos.as_inner() >= rhs.nanos.as_inner() {
                self.nanos.as_inner() - rhs.nanos.as_inner()
            } else if let Some(sub_secs) = secs.checked_sub(1) {
                secs = sub_secs;
                self.nanos.as_inner() + NANOS_PER_SEC - rhs.nanos.as_inner()
            } else {
                return None;
            };
            debug_assert!(nanos < NANOS_PER_SEC);
            Some(Duration::new(secs, nanos))
        } else {
            None
        }
    }
