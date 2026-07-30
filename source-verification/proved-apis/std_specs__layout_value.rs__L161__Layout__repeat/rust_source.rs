pub const fn repeat(&self, n: usize) -> Result<(Self, usize), LayoutError> {
        // FIXME(const-hack): the following could be way shorter with `?`
        let padded = self.pad_to_align();
        let Ok(result) = (if let Some(k) = n.checked_sub(1) {
            let Ok(repeated) = padded.repeat_packed(k) else {
                return Err(LayoutError);
            };
            repeated.extend_packed(*self)
        } else {
            debug_assert!(n == 0);
            self.repeat_packed(0)
        }) else {
            return Err(LayoutError);
        };
        Ok((result, padded.size()))
    }
