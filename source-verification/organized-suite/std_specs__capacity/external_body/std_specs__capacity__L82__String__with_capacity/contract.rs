pub assume_specification[ String::with_capacity ](capacity: usize) -> (result: String)
    ensures
        result@ == Seq::<char>::empty(),
        result.spec_capacity() >= capacity as nat,
;
