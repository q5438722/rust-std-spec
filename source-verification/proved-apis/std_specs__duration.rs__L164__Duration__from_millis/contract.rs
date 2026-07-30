pub assume_specification[ Duration::from_millis ](millis: u64) -> (result: Duration)
    ensures
        result@ == millis as nat * 1_000_000,
;
