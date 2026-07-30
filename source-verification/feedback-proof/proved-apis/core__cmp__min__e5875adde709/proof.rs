#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::cmp::OrdSpec;

verus! {

pub fn source_cmp_min<T: core::cmp::Ord>(
    v1: T,
    v2: T,
) -> (r: T)
    requires
        T::obeys_cmp_spec(),
    ensures
        match v2.cmp_spec(&v1) {
            core::cmp::Ordering::Less => r == v2,
            core::cmp::Ordering::Equal => r == v1,
            core::cmp::Ordering::Greater => r == v1,
        },
{
    v1.min(v2)
}

} // verus!

fn main() {}