#![allow(dead_code)]

use core::alloc::Layout;
use vstd::layout::{align_of_as_usize, layout_for_type_is_valid, size_of_as_usize};
use vstd::prelude::*;
use vstd::std_specs::layout_value::*;

verus! {

fn source_layout_new<T>() -> (result: Layout)
    ensures
        result@ == (LayoutView {
            size: size_of_as_usize::<T>(),
            align: align_of_as_usize::<T>(),
        }),
{
    layout_for_type_is_valid::<T>();
    let size = core::mem::size_of::<T>();
    let align = core::mem::align_of::<T>();
    unsafe { Layout::from_size_align_unchecked(size, align) }
}

} // verus!

fn main() {}