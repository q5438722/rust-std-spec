pub assume_specification[ Duration::as_secs ](duration: &Duration) -> (result: u64)
    ensures
        result as nat == duration@ / nanos_per_second(),
;
