    pub fn fill(&mut self, value: T)
    where
        T: Clone,
    {
        specialize::SpecFill::spec_fill(self, value);
    }
