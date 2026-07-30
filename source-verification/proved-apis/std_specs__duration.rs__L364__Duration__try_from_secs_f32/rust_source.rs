pub fn try_from_secs_f32(secs: f32) -> Result<Duration, TryFromFloatSecsError> {
        try_from_secs!(
            secs = secs,
            mantissa_bits = 23,
            exponent_bits = 8,
            offset = 41,
            bits_ty = u32,
            double_ty = u64,
        )
    }
