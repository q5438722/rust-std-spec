pub assume_specification[ Ordering::is_le ](ordering: Ordering) -> (result: bool)
    ensures
        result <==> !(ordering is Greater),
;
