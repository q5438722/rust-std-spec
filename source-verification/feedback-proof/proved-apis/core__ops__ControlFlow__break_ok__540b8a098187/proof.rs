#![allow(dead_code)]

use core::ops::ControlFlow;
use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_control_flow_break_ok<B, C>(
    flow: ControlFlow<B, C>,
) -> (result: Result<B, C>)
    ensures
        result == match flow {
            ControlFlow::Continue(c) => Err(c),
            ControlFlow::Break(b) => Ok(b),
        },
{
    match flow {
        ControlFlow::Continue(c) => Err(c),
        ControlFlow::Break(b) => Ok(b),
    }
}

} // verus!

fn main() {}