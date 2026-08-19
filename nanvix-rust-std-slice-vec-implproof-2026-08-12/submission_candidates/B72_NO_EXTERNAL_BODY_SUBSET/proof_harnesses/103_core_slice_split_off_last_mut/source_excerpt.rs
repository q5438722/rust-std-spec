    pub const fn split_off_last_mut<'a>(self: &mut &'a mut Self) -> Option<&'a mut T> {
        // FIXME(const-hack): Use `mem::take` and `?` when available in const.
        // Original: `mem::take(self).split_last_mut()?`
        let Some((last, rem)) = mem::replace(self, &mut []).split_last_mut() else { return None };
        *self = rem;
        Some(last)
    }
