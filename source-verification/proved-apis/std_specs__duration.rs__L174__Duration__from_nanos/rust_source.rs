pub const fn from_nanos(nanos: u64) -> Duration {
        const NANOS_PER_SEC: u64 = self::NANOS_PER_SEC as u64;
        let secs = nanos / NANOS_PER_SEC;
        let subsec_nanos = (nanos % NANOS_PER_SEC) as u32;
        // SAFETY: x % 1_000_000_000 < 1_000_000_000
        let subsec_nanos = unsafe { Nanoseconds::new_unchecked(subsec_nanos) };

        Duration { secs, nanos: subsec_nanos }
    }
