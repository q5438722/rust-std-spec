pub assume_specification[ Ordering::is_lt ](ordering: Ordering) -> (result: bool)
    ensures
        result <==> ordering is Less,
;
