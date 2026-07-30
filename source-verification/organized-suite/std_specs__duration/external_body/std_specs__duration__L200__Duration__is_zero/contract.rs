pub assume_specification[ Duration::is_zero ](duration: &Duration) -> (result: bool)
    ensures
        result <==> duration@ == 0,
;
