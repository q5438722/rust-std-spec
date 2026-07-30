#![allow(dead_code)]

use core::ops::ControlFlow;
use vstd::prelude::*;

verus! {

pub fn source_control_flow_map_continue<B, C, T, F>(
    flow: ControlFlow<B, C>,
    f: F,
) -> (res: ControlFlow<B, T>)
where
    F: FnOnce(C) -> T,
    requires
        match flow {
            ControlFlow::Continue(c) => f.requires((c,)),
            ControlFlow::Break(_) => true,
        },
    ensures
        match flow {
            ControlFlow::Break(b) => res == ControlFlow::Break(b),
            ControlFlow::Continue(c) => match res {
                ControlFlow::Continue(t) => f.ensures((c,), t),
                ControlFlow::Break(_) => false,
            },
        },
{
    match flow {
        ControlFlow::Continue(x) => ControlFlow::Continue(f(x)),
        ControlFlow::Break(x) => ControlFlow::Break(x),
    }
}

} // verus!

fn main() {}