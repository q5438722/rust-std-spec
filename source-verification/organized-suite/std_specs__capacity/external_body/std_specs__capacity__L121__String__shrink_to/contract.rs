pub assume_specification[ String::shrink_to ](s: &mut String, min_capacity: usize)
    ensures
        final(s)@ == old(s)@,
        final(s).spec_capacity() >= encode_utf8(old(s)@).len(),
        final(s).spec_capacity() <= old(s).spec_capacity(),
;
