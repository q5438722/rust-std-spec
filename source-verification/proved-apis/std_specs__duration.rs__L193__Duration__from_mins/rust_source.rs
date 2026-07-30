pub const fn from_mins(mins: u64) -> Duration {
        if mins > u64::MAX / SECS_PER_MINUTE {
            panic!("overflow in Duration::from_mins");
        }

        Duration::from_secs(mins * SECS_PER_MINUTE)
    }
