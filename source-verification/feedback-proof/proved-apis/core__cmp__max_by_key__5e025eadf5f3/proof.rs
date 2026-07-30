#![allow(dead_code)]

use vstd::prelude::*;
use vstd::std_specs::cmp::PartialOrdSpec;

verus! {

pub fn source_max_by_key<T, F, K>(
    v1: T,
    v2: T,
    mut f: F,
) -> (result: T)
where
    F: FnMut(&T) -> K,
    K: core::cmp::Ord,
    requires
        K::obeys_partial_cmp_spec(),
        f.requires((&v2,)),
        f.requires((&v1,)),
        forall|key2a: K, key2b: K|
            #![trigger f.ensures((&v2,), key2a), f.ensures((&v2,), key2b)]
            f.ensures((&v2,), key2a)
                && f.ensures((&v2,), key2b)
                ==> key2a == key2b,
        forall|key1a: K, key1b: K|
            #![trigger f.ensures((&v1,), key1a), f.ensures((&v1,), key1b)]
            f.ensures((&v1,), key1a)
                && f.ensures((&v1,), key1b)
                ==> key1a == key1b,
    ensures
        exists|key2: K| {
            &&& #[trigger] f.ensures((&v2,), key2)
            &&& exists|key1: K| {
                &&& #[trigger] f.ensures((&v1,), key1)
                &&& result == if key2.partial_cmp_spec(&key1)
                    == Some(core::cmp::Ordering::Less)
                {
                    v1
                } else {
                    v2
                }
            }
        },
{
    if f(&v2) < f(&v1) { v1 } else { v2 }
}

} // verus!

fn main() {}