pub const fn pad_to_align(&self) -> Layout {
        // This cannot overflow. Quoting from the invariant of Layout:
        // > `size`, when rounded up to the nearest multiple of `align`,
        // > must not overflow isize (i.e., the rounded value must be
        // > less than or equal to `isize::MAX`)
        let new_size = self.size_rounded_up_to_custom_alignment(self.align);

        // SAFETY: padded size is guaranteed to not exceed `isize::MAX`.
        unsafe { Layout::from_size_alignment_unchecked(new_size, self.alignment()) }
    }
