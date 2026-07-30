#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_option_xor<T>(
    option: Option<T>,
    optb: Option<T>,
) -> (res: Option<T>)
    ensures
        res == match (option, optb) {
            (Some(a), None) => Some(a),
            (None, Some(b)) => Some(b),
            _ => None,
        },
    no_unwind
{
    match (option, optb) {
        (a @ Some(_), None) => a,
        (None, b @ Some(_)) => b,
        _ => None,
    }
}

} // verus!

fn main() {}