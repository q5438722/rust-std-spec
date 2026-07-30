#![allow(dead_code)]

use core::time::Duration;
use vstd::prelude::*;
use vstd::std_specs::duration::*;

verus! {

fn source_duration_abs_diff(lhs: Duration, rhs: Duration) -> (result: Duration)
    ensures
        result@ == if lhs@ >= rhs@ {
            lhs@ - rhs@
        } else {
            rhs@ - lhs@
        },
{
    if let Some(res) = lhs.checked_sub(rhs) {
        res
    } else {
        rhs.checked_sub(lhs).unwrap()
    }
}

} // verus!

fn main() {}