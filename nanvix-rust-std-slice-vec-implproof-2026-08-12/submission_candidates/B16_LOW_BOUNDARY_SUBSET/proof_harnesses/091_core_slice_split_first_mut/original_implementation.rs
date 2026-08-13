// Original Rust 1.96 implementation before Verus mutable slice-pattern desugaring.
// Source: core/src/slice/mod.rs:220-222
pub const fn split_first_mut(&mut self) -> Option<(&mut T, &mut [T])> {
    if let [first, tail @ ..] = self { Some((first, tail)) } else { None }
}
