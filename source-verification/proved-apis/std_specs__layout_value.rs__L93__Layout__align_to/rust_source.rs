pub const fn align_to(&self, align: usize) -> Result<Self, LayoutError> {
        if let Some(alignment) = Alignment::new(align) {
            self.adjust_alignment_to(alignment)
        } else {
            Err(LayoutError)
        }
    }
