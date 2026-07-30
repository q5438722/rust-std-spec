pub assume_specification[ DefaultHasher::new ]() -> (result: DefaultHasher)
    ensures
        result@ == Seq::<Seq<u8>>::empty(),
;
