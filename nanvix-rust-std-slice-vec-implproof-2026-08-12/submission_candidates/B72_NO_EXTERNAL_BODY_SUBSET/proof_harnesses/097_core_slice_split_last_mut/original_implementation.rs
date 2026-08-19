// Original Rust 1.96 implementation before Verus mutable slice-pattern desugaring.
// Source: core/src/slice/mod.rs:262-264
pub const fn split_last_mut(&mut self) -> Option<(&mut T, &mut [T])> {
    if let [init @ .., last] = self { Some((last, init)) } else { None }
}
