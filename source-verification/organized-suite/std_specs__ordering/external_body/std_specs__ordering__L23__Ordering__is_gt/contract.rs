pub assume_specification[ Ordering::is_gt ](ordering: Ordering) -> (result: bool)
    ensures
        result <==> ordering is Greater,
;
