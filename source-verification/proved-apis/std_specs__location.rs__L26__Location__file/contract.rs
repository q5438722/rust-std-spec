pub assume_specification<'a>[ Location::file ](location: &Location<'a>) -> (result: &'a str)
    ensures
        result@ == location@.file,
;
