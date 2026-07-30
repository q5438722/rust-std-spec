pub assume_specification<'a>[ Location::line ](location: &Location<'a>) -> (result: u32)
    ensures
        result == location@.line,
;
