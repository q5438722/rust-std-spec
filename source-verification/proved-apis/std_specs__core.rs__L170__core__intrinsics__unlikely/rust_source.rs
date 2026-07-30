pub const fn unlikely(b: bool) -> bool {
    if b {
        cold_path();
        true
    } else {
        false
    }
}
