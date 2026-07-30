pub const fn from_micros(micros: u64) -> Duration {
        let secs = micros / MICROS_PER_SEC;
        let subsec_micros = (micros % MICROS_PER_SEC) as u32;
        // SAFETY: (x % 1_000_000) * 1_000 < 1_000_000_000
        //         => x % 1_000_000 < 1_000_000
        let subsec_nanos = unsafe { Nanoseconds::new_unchecked(subsec_micros * NANOS_PER_MICRO) };

        Duration { secs, nanos: subsec_nanos }
    }
