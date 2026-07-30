pub assume_specification[ String::shrink_to_fit ](s: &mut String)
    ensures
        final(s)@ == old(s)@,
        final(s).spec_capacity() >= encode_utf8(old(s)@).len(),
        final(s).spec_capacity() <= old(s).spec_capacity(),
;
