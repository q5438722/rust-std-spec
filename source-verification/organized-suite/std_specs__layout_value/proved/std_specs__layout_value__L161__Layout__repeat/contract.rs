pub assume_specification[ Layout::repeat ](layout: &Layout, n: usize) -> (result: Result<
    (Layout, usize),
    LayoutError,
>)
    ensures
        ({
            let stride = round_up_to(layout@.size as nat, layout@.align as nat);
            let size = if n == 0 {
                0
            } else {
                stride * (n as nat - 1) + layout@.size as nat
            };
            size <= usize::MAX as nat && valid_layout(size as usize, layout@.align)
        }) ==> ({
            let stride = round_up_to(layout@.size as nat, layout@.align as nat);
            let size = if n == 0 {
                0
            } else {
                stride * (n as nat - 1) + layout@.size as nat
            };
            result matches Ok(pair) && pair.0@ == (LayoutView {
                size: size as usize,
                align: layout@.align,
            }) && pair.1 as nat == stride
        }),
        ({
            let stride = round_up_to(layout@.size as nat, layout@.align as nat);
            let size = if n == 0 {
                0
            } else {
                stride * (n as nat - 1) + layout@.size as nat
            };
            size > usize::MAX as nat || !valid_layout(size as usize, layout@.align)
        }) ==> result is Err,
;
