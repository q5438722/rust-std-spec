pub const fn insert(&mut self, value: T) -> &mut T
    where
        T: [const] Destruct,
    {
        *self = Some(value);

        // SAFETY: the code above just filled the option
        unsafe { self.as_mut().unwrap_unchecked() }
    }
