pub const fn from_hours(hours: u64) -> Duration {
        if hours > u64::MAX / (SECS_PER_MINUTE * MINS_PER_HOUR) {
            panic!("overflow in Duration::from_hours");
        }

        Duration::from_secs(hours * MINS_PER_HOUR * SECS_PER_MINUTE)
    }
