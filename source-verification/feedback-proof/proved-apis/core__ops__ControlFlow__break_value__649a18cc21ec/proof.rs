#![allow(dead_code)]

use core::ops::ControlFlow;
use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_control_flow_break_value<B, C>(
    flow: ControlFlow<B, C>,
) -> (result: Option<B>)
    ensures
        result == match flow {
            ControlFlow::Continue(_) => None,
            ControlFlow::Break(b) => Some(b),
        },
{
    match flow {
        ControlFlow::Continue(..) => None,
        ControlFlow::Break(x) => Some(x),
    }
}

} // verus!

fn main() {}