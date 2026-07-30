pub assume_specification[ Duration::as_millis ](duration: &Duration) -> (result: u128)
    ensures
        result as nat == duration@ / 1_000_000,
;
