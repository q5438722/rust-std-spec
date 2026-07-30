pub assume_specification[ Duration::from_nanos_u128 ](nanos: u128) -> (result: Duration)
    requires
        nanos as nat <= duration_max_nanos(),
    ensures
        result@ == nanos as nat,
;
