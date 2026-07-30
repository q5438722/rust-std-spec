pub assume_specification[ Layout::repeat_packed ](layout: &Layout, n: usize) -> (result: Result<
    Layout,
    LayoutError,
>)
    ensures
        ({
            let size = layout@.size as nat * n as nat;
            size <= usize::MAX as nat && valid_layout(size as usize, layout@.align)
        }) ==> (result matches Ok(new_layout) && new_layout@ == (LayoutView {
            size: (layout@.size as nat * n as nat) as usize,
            align: layout@.align,
        })),
        ({
            let size = layout@.size as nat * n as nat;
            size > usize::MAX as nat || !valid_layout(size as usize, layout@.align)
        }) ==> result is Err,
;
