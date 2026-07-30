#![allow(dead_code)]

use vstd::prelude::*;

verus! {

pub fn source_max_by<T, F>(
    v1: T,
    v2: T,
    compare: F,
) -> (result: T)
where
    F: FnOnce(&T, &T) -> core::cmp::Ordering,
    requires
        compare.requires((&v1, &v2)),
        forall|ordering1: core::cmp::Ordering, ordering2: core::cmp::Ordering|
            #![trigger compare.ensures((&v1, &v2), ordering1),
                       compare.ensures((&v1, &v2), ordering2)]
            compare.ensures((&v1, &v2), ordering1)
                && compare.ensures((&v1, &v2), ordering2)
                ==> (ordering1 == core::cmp::Ordering::Greater
                    <==> ordering2 == core::cmp::Ordering::Greater),
    ensures
        exists|ordering: core::cmp::Ordering| {
            &&& #[trigger] compare.ensures((&v1, &v2), ordering)
            &&& result == if ordering == core::cmp::Ordering::Greater { v1 } else { v2 }
        },
{
    if compare(&v1, &v2).is_gt() { v1 } else { v2 }
}

} // verus!

fn main() {}