pub const fn from_nanos_u128(nanos: u128) -> Duration {
        const NANOS_PER_SEC: u128 = self::NANOS_PER_SEC as u128;
        let Ok(secs) = u64::try_from(nanos / NANOS_PER_SEC) else {
            panic!("overflow in `Duration::from_nanos_u128`");
        };
        let subsec_nanos = (nanos % NANOS_PER_SEC) as u32;
        // SAFETY: x % 1_000_000_000 < 1_000_000_000 also, subsec_nanos >= 0 since u128 >=0 and u32 >=0
        let subsec_nanos = unsafe { Nanoseconds::new_unchecked(subsec_nanos) };

        Duration { secs: secs as u64, nanos: subsec_nanos }
    }
