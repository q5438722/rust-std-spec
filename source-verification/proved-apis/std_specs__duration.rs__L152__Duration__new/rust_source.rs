pub const fn new(secs: u64, nanos: u32) -> Duration {
        if nanos < NANOS_PER_SEC {
            // SAFETY: nanos < NANOS_PER_SEC, therefore nanos is within the valid range
            Duration { secs, nanos: unsafe { Nanoseconds::new_unchecked(nanos) } }
        } else {
            let secs = secs
                .checked_add((nanos / NANOS_PER_SEC) as u64)
                .expect("overflow in Duration::new");
            let nanos = nanos % NANOS_PER_SEC;
            // SAFETY: nanos % NANOS_PER_SEC < NANOS_PER_SEC, therefore nanos is within the valid range
            Duration { secs, nanos: unsafe { Nanoseconds::new_unchecked(nanos) } }
        }
    }
