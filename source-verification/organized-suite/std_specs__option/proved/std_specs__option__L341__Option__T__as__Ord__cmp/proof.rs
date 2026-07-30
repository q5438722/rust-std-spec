#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::{Ord, Ordering};
use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::cmp::*;
use vstd::std_specs::option::*;

verus! {

fn option_cmp_proof<T: Ord>(
    x: &Option<T>,
    y: &Option<T>,
) -> (res: Ordering)
    ensures
        <Option<T> as OrdSpec>::obeys_cmp_spec() ==>
            res == <Option<T> as OrdSpec>::cmp_spec(x, y),
{
    match (x, y) {
        (Some(l), Some(r)) => l.cmp(r),
        (Some(_), None) => Ordering::Greater,
        (None, Some(_)) => Ordering::Less,
        (None, None) => Ordering::Equal,
    }
}

}

fn main() {}