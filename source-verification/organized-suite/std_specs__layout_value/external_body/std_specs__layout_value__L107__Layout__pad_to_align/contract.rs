pub assume_specification[ Layout::pad_to_align ](layout: &Layout) -> (result: Layout)
    ensures
        result@.align == layout@.align,
        result@.size as nat == round_up_to(layout@.size as nat, layout@.align as nat),
;
