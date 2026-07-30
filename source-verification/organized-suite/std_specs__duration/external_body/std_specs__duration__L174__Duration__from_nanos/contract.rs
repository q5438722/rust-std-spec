pub assume_specification[ Duration::from_nanos ](nanos: u64) -> (result: Duration)
    ensures
        result@ == nanos as nat,
;
