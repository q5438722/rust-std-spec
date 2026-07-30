pub const fn from_millis(millis: u64) -> Duration {
        let secs = millis / MILLIS_PER_SEC;
        let subsec_millis = (millis % MILLIS_PER_SEC) as u32;
        // SAFETY: (x % 1_000) * 1_000_000 < 1_000_000_000
        //         => x % 1_000 < 1_000
        let subsec_nanos = unsafe { Nanoseconds::new_unchecked(subsec_millis * NANOS_PER_MILLI) };

        Duration { secs, nanos: subsec_nanos }
    }
