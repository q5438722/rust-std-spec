// Original Rust 1.96 implementation before method-call/let-else harness lowering.
// Source: core/src/slice/mod.rs:5060-5065
pub const fn split_off_last<'a>(self: &mut &'a Self) -> Option<&'a T> {
    // FIXME(const-hack): Use `?` when available in const instead of `let-else`.
    let Some((last, rem)) = self.split_last() else { return None };
    *self = rem;
    Some(last)
}
