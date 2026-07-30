#![allow(dead_code)]

use core::ops::ControlFlow;
use core::result::Result;
use vstd::prelude::*;

verus! {

fn source_control_flow_continue_ok<B, C>(
    flow: ControlFlow<B, C>,
) -> (result: Result<C, B>)
    ensures
        result == match flow {
            ControlFlow::Continue(c) => Ok(c),
            ControlFlow::Break(b) => Err(b),
        },
    no_unwind
{
    match flow {
        ControlFlow::Continue(c) => Ok(c),
        ControlFlow::Break(b) => Err(b),
    }
}

} // verus!

fn main() {}