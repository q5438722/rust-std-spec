#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn option_map_proof<T, U, F: FnOnce(T) -> U>(
    a: Option<T>,
    f: F,
) -> (ret: Option<U>)
    requires
        a.is_some() ==> f.requires((a.unwrap(),)),
    ensures
        ret.is_some() == a.is_some(),
        ret.is_some() ==> f.ensures((a.unwrap(),), ret.unwrap()),
{
    match a {
        Some(x) => Some(f(x)),
        None => None,
    }
}

} // verus!

fn main() {}