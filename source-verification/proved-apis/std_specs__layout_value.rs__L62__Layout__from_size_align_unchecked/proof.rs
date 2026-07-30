#![allow(dead_code)]

use core::alloc::Layout;
use vstd::layout::valid_layout;
use vstd::prelude::*;
use vstd::std_specs::layout_value::*;

verus! {

unsafe fn source_layout_from_size_align_unchecked(
    size: usize,
    align: usize,
) -> (result: Layout)
    requires
        valid_layout(size, align),
    ensures
        result@ == (LayoutView { size, align }),
{
    // Rust 1.96's checked sibling uses the same predicate and field construction.
    let result = Layout::from_size_align(size, align);
    assert(result is Ok);
    result.unwrap()
}

} // verus!

fn main() {}