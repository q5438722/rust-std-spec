pub const unsafe fn unreachable_unchecked() -> ! {
    ub_checks::assert_unsafe_precondition!(
        check_language_ub,
        "hint::unreachable_unchecked must never be reached",
        () => false
    );
    // SAFETY: the safety contract for `intrinsics::unreachable` must
    // be upheld by the caller.
    unsafe { intrinsics::unreachable() }
}
