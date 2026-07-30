pub assume_specification<'a>[ String::as_str ](s: &'a String) -> (res: &'a str)
    ensures
        res@ == s@,
;
