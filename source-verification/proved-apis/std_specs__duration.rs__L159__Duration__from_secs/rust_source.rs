pub const fn from_secs(secs: u64) -> Duration {
        Duration { secs, nanos: Nanoseconds::ZERO }
    }
