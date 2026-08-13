    pub const fn split_off_first<'a>(self: &mut &'a Self) -> Option<&'a T> {
        // FIXME(const-hack): Use `?` when available in const instead of `let-else`.
        let Some((first, rem)) = self.split_first() else { return None };
        *self = rem;
        Some(first)
    }
