pub assume_specification[ String::new ]() -> (res: String)
    ensures
        res@ == Seq::<char>::empty(),
;
