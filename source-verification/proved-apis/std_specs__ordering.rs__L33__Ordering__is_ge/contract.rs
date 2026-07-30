pub assume_specification[ Ordering::is_ge ](ordering: Ordering) -> (result: bool)
    ensures
        result <==> !(ordering is Less),
;
