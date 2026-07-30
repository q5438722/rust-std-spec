#![allow(dead_code)]

use core::ops::ControlFlow;
use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_control_flow_continue_value<B, C>(
    flow: ControlFlow<B, C>,
) -> (result: Option<C>)
    ensures
        result == match flow {
            ControlFlow::Continue(c) => Some(c),
            ControlFlow::Break(_) => None,
        },
{
    match flow {
        ControlFlow::Continue(x) => Some(x),
        ControlFlow::Break(..) => None,
    }
}

} // verus!

fn main() {}