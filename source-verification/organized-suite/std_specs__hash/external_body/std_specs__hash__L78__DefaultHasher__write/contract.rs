pub assume_specification[ DefaultHasher::write ](state: &mut DefaultHasher, bytes: &[u8])
    ensures
        final(state)@ == old(state)@.push(bytes@),
;
