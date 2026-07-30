pub assume_specification[ Layout::from_size_align ](size: usize, align: usize) -> (result: Result<
    Layout,
    LayoutError,
>)
    ensures
        valid_layout(size, align) ==> (result matches Ok(layout) && layout@ == (LayoutView {
            size,
            align,
        })),
        !valid_layout(size, align) ==> result is Err,
;
