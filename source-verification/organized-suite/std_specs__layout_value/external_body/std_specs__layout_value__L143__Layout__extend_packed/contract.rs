pub assume_specification[ Layout::extend_packed ](layout: &Layout, next: Layout) -> (result: Result<
    Layout,
    LayoutError,
>)
    ensures
        ({
            let size = layout@.size as nat + next@.size as nat;
            size <= usize::MAX as nat && valid_layout(size as usize, layout@.align)
        }) ==> (result matches Ok(new_layout) && new_layout@ == (LayoutView {
            size: (layout@.size as nat + next@.size as nat) as usize,
            align: layout@.align,
        })),
        ({
            let size = layout@.size as nat + next@.size as nat;
            size > usize::MAX as nat || !valid_layout(size as usize, layout@.align)
        }) ==> result is Err,
;
