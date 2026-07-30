pub fn try_from_secs_f64(secs: f64) -> Result<Duration, TryFromFloatSecsError> {
        try_from_secs!(
            secs = secs,
            mantissa_bits = 52,
            exponent_bits = 11,
            offset = 44,
            bits_ty = u64,
            double_ty = u128,
        )
    }
