pub assume_specification[ Layout::align ](layout: &Layout) -> (result: usize)
    ensures
        result == layout@.align,
;
