pub assume_specification[ Layout::extend ](layout: &Layout, next: Layout) -> (result: Result<
    (Layout, usize),
    LayoutError,
>)
    ensures
        ({
            let offset = round_up_to(layout@.size as nat, next@.align as nat);
            let size = offset + next@.size as nat;
            size <= usize::MAX as nat && valid_layout(
                size as usize,
                max_usize(layout@.align, next@.align),
            )
        }) ==> ({
            let offset = round_up_to(layout@.size as nat, next@.align as nat);
            let size = offset + next@.size as nat;
            result matches Ok(pair) && pair.0@ == (LayoutView {
                size: size as usize,
                align: max_usize(layout@.align, next@.align),
            }) && pair.1 as nat == offset
        }),
        ({
            let offset = round_up_to(layout@.size as nat, next@.align as nat);
            let size = offset + next@.size as nat;
            size > usize::MAX as nat || !valid_layout(
                size as usize,
                max_usize(layout@.align, next@.align),
            )
        }) ==> result is Err,
;
