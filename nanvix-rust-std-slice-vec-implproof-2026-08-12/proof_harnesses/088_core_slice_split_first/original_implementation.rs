// Original Rust 1.96 implementation before Verus slice-pattern desugaring.
// Source: core/src/slice/mod.rs:198-200
pub const fn split_first(&self) -> Option<(&T, &[T])> {
    if let [first, tail @ ..] = self { Some((first, tail)) } else { None }
}
