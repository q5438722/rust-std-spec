pub const fn checked_div(self, rhs: u32) -> Option<Duration> {
        if rhs != 0 {
            let (secs, extra_secs) = (self.secs / (rhs as u64), self.secs % (rhs as u64));
            let (mut nanos, extra_nanos) =
                (self.nanos.as_inner() / rhs, self.nanos.as_inner() % rhs);
            nanos +=
                ((extra_secs * (NANOS_PER_SEC as u64) + extra_nanos as u64) / (rhs as u64)) as u32;
            debug_assert!(nanos < NANOS_PER_SEC);
            Some(Duration::new(secs, nanos))
        } else {
            None
        }
    }
