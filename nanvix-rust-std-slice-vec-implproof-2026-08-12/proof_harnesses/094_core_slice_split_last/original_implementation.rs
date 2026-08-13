// Original Rust 1.96 implementation before Verus slice-pattern desugaring.
// Source: core/src/slice/mod.rs:240-242
pub const fn split_last(&self) -> Option<(&T, &[T])> {
    if let [init @ .., last] = self { Some((last, init)) } else { None }
}
