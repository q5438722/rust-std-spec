pub const unsafe fn from_size_align_unchecked(size: usize, align: usize) -> Self {
        assert_unsafe_precondition!(
            check_library_ub,
            "Layout::from_size_align_unchecked requires that align is a power of 2 \
            and the rounded-up allocation size does not exceed isize::MAX",
            (
                size: usize = size,
                align: usize = align,
            ) => Layout::is_size_align_valid(size, align)
        );
        // SAFETY: the caller is required to uphold the preconditions.
        unsafe { Layout { size, align: mem::transmute(align) } }
    }
