pub assume_specification[ Ordering::is_ne ](ordering: Ordering) -> (result: bool)
    ensures
        result <==> !(ordering is Equal),
;
