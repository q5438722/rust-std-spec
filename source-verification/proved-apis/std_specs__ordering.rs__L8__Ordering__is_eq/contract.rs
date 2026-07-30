pub assume_specification[ Ordering::is_eq ](ordering: Ordering) -> (result: bool)
    ensures
        result <==> ordering is Equal,
;
