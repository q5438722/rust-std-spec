#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::clone::*;

verus! {

#[allow(suspicious_double_ref_op)]
fn ref_clone_proof<'b, T: core::marker::PointeeSized, 'a>(
    b: &'a &'b T,
) -> (res: &'b T)
    ensures
        res == b,
{
    b
}

}

fn main() {}