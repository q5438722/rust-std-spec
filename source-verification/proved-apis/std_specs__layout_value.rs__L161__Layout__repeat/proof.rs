#![allow(dead_code)]

use core::alloc::{Layout, LayoutError};
use vstd::layout::valid_layout;
use vstd::prelude::*;
use vstd::std_specs::layout_value::*;

#[cfg(verus_keep_ghost)]
macro_rules! debug_assert {
    ($condition:expr $(,)?) => {
        proof! {
            assert($condition);
        }
    };
}

verus! {

fn source_layout_repeat(
    layout: &Layout,
    n: usize,
) -> (result: Result<(Layout, usize), LayoutError>)
    ensures
        ({
            let stride = round_up_to(layout@.size as nat, layout@.align as nat);
            let size = if n == 0 {
                0
            } else {
                stride * (n as nat - 1) + layout@.size as nat
            };
            size <= usize::MAX as nat && valid_layout(size as usize, layout@.align)
        }) ==> ({
            let stride = round_up_to(layout@.size as nat, layout@.align as nat);
            let size = if n == 0 {
                0
            } else {
                stride * (n as nat - 1) + layout@.size as nat
            };
            result matches Ok(pair) && pair.0@ == (LayoutView {
                size: size as usize,
                align: layout@.align,
            }) && pair.1 as nat == stride
        }),
        ({
            let stride = round_up_to(layout@.size as nat, layout@.align as nat);
            let size = if n == 0 {
                0
            } else {
                stride * (n as nat - 1) + layout@.size as nat
            };
            size > usize::MAX as nat || !valid_layout(size as usize, layout@.align)
        }) ==> result is Err,
{
    let padded = layout.pad_to_align();
    let repeat_result = if let Some(k) = n.checked_sub(1) {
        match padded.repeat_packed(k) {
            Ok(repeated) => repeated.extend_packed(*layout),
            Err(error) => return Err(error),
        }
    } else {
        debug_assert!(n == 0);
        layout.repeat_packed(0)
    };
    let result = match repeat_result {
        Ok(result) => result,
        Err(error) => return Err(error),
    };
    Ok((result, padded.size()))
}

} // verus!

fn main() {}