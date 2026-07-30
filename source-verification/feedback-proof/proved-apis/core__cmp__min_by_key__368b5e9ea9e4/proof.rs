#![allow(dead_code)]

use vstd::prelude::*;

verus! {

pub fn source_min_by_key<T, F, K>(
    v1: T,
    v2: T,
    mut f: F,
) -> (result: T)
where
    F: FnMut(&T) -> K,
    K: core::cmp::Ord,
    requires
        f.requires((&v2,)),
        f.requires((&v1,)),
    ensures
        exists|key2: K| {
            &&& #[trigger] f.ensures((&v2,), key2)
            &&& exists|key1: K| {
                &&& #[trigger] f.ensures((&v1,), key1)
                &&& exists|is_less: bool| {
                    &&& #[trigger] call_ensures(
                        <K as core::cmp::PartialOrd>::lt,
                        (&key2, &key1),
                        is_less,
                    )
                    &&& result == if is_less { v2 } else { v1 }
                }
            }
        },
{
    if f(&v2) < f(&v1) { v2 } else { v1 }
}

} // verus!

fn main() {}