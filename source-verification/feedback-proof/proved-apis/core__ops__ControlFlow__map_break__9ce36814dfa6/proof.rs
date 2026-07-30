#![allow(dead_code)]

use core::ops::ControlFlow;
use vstd::prelude::*;

verus! {

pub fn source_control_flow_map_break<B, C, T, F>(
    flow: ControlFlow<B, C>,
    f: F,
) -> (res: ControlFlow<T, C>)
where
    F: FnOnce(B) -> T,
    requires
        match flow {
            ControlFlow::Break(b) => f.requires((b,)),
            ControlFlow::Continue(_) => true,
        },
    ensures
        match flow {
            ControlFlow::Continue(c) => res == ControlFlow::Continue(c),
            ControlFlow::Break(b) => match res {
                ControlFlow::Break(t) => f.ensures((b,), t),
                ControlFlow::Continue(_) => false,
            },
        },
{
    match flow {
        ControlFlow::Continue(x) => ControlFlow::Continue(x),
        ControlFlow::Break(x) => ControlFlow::Break(f(x)),
    }
}

} // verus!

fn main() {}