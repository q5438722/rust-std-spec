pub assume_specification[ <String as PartialEq>::eq ](s: &String, other: &String) -> (res: bool)
    ensures
        res == (s@ == other@),
;
