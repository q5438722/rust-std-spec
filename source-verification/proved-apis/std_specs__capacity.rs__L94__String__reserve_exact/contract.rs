pub assume_specification[ String::reserve_exact ](s: &mut String, additional: usize)
    ensures
        final(s)@ == old(s)@,
        final(s).spec_capacity() >= encode_utf8(old(s)@).len() + additional as nat,
;
