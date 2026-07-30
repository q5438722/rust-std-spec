pub assume_specification[ Layout::from_size_align_unchecked ](size: usize, align: usize) -> (result:
    Layout)
    requires
        valid_layout(size, align),
    ensures
        result@ == (LayoutView { size, align }),
;
