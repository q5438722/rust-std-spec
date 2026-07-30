pub assume_specification[ String::try_reserve_exact ](s: &mut String, additional: usize) -> (result:
    Result<(), TryReserveError>)
    ensures
        final(s)@ == old(s)@,
        result is Ok ==> final(s).spec_capacity() >= encode_utf8(old(s)@).len() + additional as nat,
;
