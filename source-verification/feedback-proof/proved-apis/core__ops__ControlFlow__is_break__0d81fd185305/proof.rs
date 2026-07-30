#![allow(dead_code)]

use core::ops::ControlFlow;
use vstd::prelude::*;

verus! {

pub fn source_control_flow_is_break<B, C>(
    flow: &ControlFlow<B, C>,
) -> (result: bool)
    ensures
        result <==> flow is Break,
    no_unwind
{
    match *flow {
        ControlFlow::Break(_) => true,
        _ => false,
    }
}

} // verus!

fn main() {}