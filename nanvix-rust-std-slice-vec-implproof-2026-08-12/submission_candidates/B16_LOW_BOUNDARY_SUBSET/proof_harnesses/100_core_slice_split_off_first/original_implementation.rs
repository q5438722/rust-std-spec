// Original Rust 1.96 implementation before method-call/let-else harness lowering.
// Source: core/src/slice/mod.rs:5010-5015
pub const fn split_off_first<'a>(self: &mut &'a Self) -> Option<&'a T> {
    // FIXME(const-hack): Use `?` when available in const instead of `let-else`.
    let Some((first, rem)) = self.split_first() else { return None };
    *self = rem;
    Some(first)
}
