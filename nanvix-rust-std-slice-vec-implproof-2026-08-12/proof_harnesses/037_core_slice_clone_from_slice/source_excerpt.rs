    pub const fn clone_from_slice(&mut self, src: &[T])
    where
        T: [const] Clone + [const] Destruct,
    {
        self.spec_clone_from(src);
    }
