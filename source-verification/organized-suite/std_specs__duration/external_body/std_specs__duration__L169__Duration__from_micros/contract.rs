pub assume_specification[ Duration::from_micros ](micros: u64) -> (result: Duration)
    ensures
        result@ == micros as nat * 1_000,
;
