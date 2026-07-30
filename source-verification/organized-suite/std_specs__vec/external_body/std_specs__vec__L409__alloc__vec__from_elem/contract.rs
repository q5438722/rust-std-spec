pub assume_specification<T: Clone>[ alloc::vec::from_elem ](elem: T, n: usize) -> (v: Vec<T>)
    ensures
        v.len() == n,
        forall |i| 0 <= i < n ==> cloned(elem, #[trigger] v@[i]);
