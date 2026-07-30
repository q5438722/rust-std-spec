pub assume_specification<'a>[ Location::column ](location: &Location<'a>) -> (result: u32)
    ensures
        result == location@.column,
;
