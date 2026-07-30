pub const fn checked_add(self, rhs: Duration) -> Option<Duration> {
        if let Some(mut secs) = self.secs.checked_add(rhs.secs) {
            let mut nanos = self.nanos.as_inner() + rhs.nanos.as_inner();
            if nanos >= NANOS_PER_SEC {
                nanos -= NANOS_PER_SEC;
                let Some(new_secs) = secs.checked_add(1) else {
                    return None;
                };
                secs = new_secs;
            }
            debug_assert!(nanos < NANOS_PER_SEC);
            Some(Duration::new(secs, nanos))
        } else {
            None
        }
    }
