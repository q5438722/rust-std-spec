pub assume_specification[ Layout::size ](layout: &Layout) -> (result: usize)
    ensures
        result == layout@.size,
;
