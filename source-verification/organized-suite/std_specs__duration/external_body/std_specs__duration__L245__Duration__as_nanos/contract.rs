pub assume_specification[ Duration::as_nanos ](duration: &Duration) -> (result: u128)
    ensures
        result as nat == duration@,
;
