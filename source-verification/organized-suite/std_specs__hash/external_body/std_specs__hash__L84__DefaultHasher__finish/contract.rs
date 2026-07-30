pub assume_specification[ DefaultHasher::finish ](state: &DefaultHasher) -> (result: u64)
    ensures
        result == DefaultHasher::spec_finish(state@),
;
