pub assume_specification<Key: Eq + Hash, S: BuildHasher, A: Allocator>[ HashSet::<
    Key,
    S,
    A,
>::reserve ](m: &mut HashSet<Key, S, A>, additional: usize)
    ensures
        final(m)@ == old(m)@,
;
