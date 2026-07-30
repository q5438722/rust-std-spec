#![allow(dead_code)]

use core::ops::ControlFlow;
use vstd::prelude::*;

verus! {

pub fn source_control_flow_is_continue<B, C>(
    flow: &ControlFlow<B, C>,
) -> (result: bool)
    ensures
        result <==> flow is Continue,
{
    matches!(*flow, ControlFlow::Continue(_))
}

} // verus!

fn main() {}