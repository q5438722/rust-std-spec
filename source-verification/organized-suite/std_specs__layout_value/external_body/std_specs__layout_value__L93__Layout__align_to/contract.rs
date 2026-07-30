pub assume_specification[ Layout::align_to ](layout: &Layout, align: usize) -> (result: Result<
    Layout,
    LayoutError,
>)
    ensures
        valid_layout(0, align) && valid_layout(layout@.size, max_usize(layout@.align, align)) ==> (
        result matches Ok(new_layout) && new_layout@ == (LayoutView {
            size: layout@.size,
            align: max_usize(layout@.align, align),
        })),
        (!valid_layout(0, align) || !valid_layout(layout@.size, max_usize(layout@.align, align)))
            ==> result is Err,
;
