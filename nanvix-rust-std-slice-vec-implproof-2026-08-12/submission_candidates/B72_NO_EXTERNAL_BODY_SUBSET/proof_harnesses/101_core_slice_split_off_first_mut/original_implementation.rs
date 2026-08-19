// Original Rust 1.96 implementation before mem::replace and pattern lowering.
// Source: core/src/slice/mod.rs:5035-5041
pub const fn split_off_first_mut<'a>(self: &mut &'a mut Self) -> Option<&'a mut T> {
    // FIXME(const-hack): Use `mem::take` and `?` when available in const.
    // Original: `mem::take(self).split_first_mut()?`
    let Some((first, rem)) = mem::replace(self, &mut []).split_first_mut() else { return None };
    *self = rem;
    Some(first)
}
