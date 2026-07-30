pub const unsafe fn new_unchecked(n: T) -> Self {
        match Self::new(n) {
            Some(n) => n,
            None => {
                // SAFETY: The caller guarantees that `n` is non-zero, so this is unreachable.
                unsafe {
                    ub_checks::assert_unsafe_precondition!(
                        check_language_ub,
                        "NonZero::new_unchecked requires the argument to be non-zero",
                        () => false,
                    );
                    intrinsics::unreachable()
                }
            }
        }
    }
