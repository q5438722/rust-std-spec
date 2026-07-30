pub const fn likely(b: bool) -> bool {
    if b {
        true
    } else {
        cold_path();
        false
    }
}
