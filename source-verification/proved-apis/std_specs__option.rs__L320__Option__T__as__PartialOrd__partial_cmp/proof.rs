#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::{Ordering, PartialOrd};
use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::cmp::PartialOrdSpec;
use vstd::std_specs::option::*;

verus! {

fn source_option_partial_cmp<T: PartialOrd>(
    x: &Option<T>,
    y: &Option<T>,
) -> (result: Option<Ordering>)
    ensures
        <Option<T> as PartialOrdSpec>::obeys_partial_cmp_spec() ==>
            result == <Option<T> as PartialOrdSpec>::partial_cmp_spec(x, y),
{
    match (x, y) {
        (Some(l), Some(r)) => l.partial_cmp(r),
        (Some(_), None) => Some(Ordering::Greater),
        (None, Some(_)) => Some(Ordering::Less),
        (None, None) => Some(Ordering::Equal),
    }
}

}

fn main() {}