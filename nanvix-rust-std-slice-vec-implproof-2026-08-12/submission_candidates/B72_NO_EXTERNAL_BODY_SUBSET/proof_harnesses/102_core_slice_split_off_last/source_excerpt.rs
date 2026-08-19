    pub const fn split_off_last<'a>(self: &mut &'a Self) -> Option<&'a T> {
        // FIXME(const-hack): Use `?` when available in const instead of `let-else`.
        let Some((last, rem)) = self.split_last() else { return None };
        *self = rem;
        Some(last)
    }
