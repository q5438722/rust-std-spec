    pub fn fill_with<F>(&mut self, mut f: F)
    where
        F: FnMut() -> T,
    {
        for el in self {
            *el = f();
        }
    }
