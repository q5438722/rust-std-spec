pub assume_specification[ str::chars ](s: &str) -> (iter: Chars<'_>)
    ensures
        iter == spec_iter(s),
        IteratorSpec::decrease(&iter) is Some,
        IteratorSpec::initial_value_relation(&iter, &iter),
;
