pub assume_specification<Key: Eq + Hash, Value, S: BuildHasher, A: Allocator>[ HashMap::<
    Key,
    Value,
    S,
    A,
>::reserve ](m: &mut HashMap<Key, Value, S, A>, additional: usize)
    ensures
        final(m)@ == old(m)@,
;
