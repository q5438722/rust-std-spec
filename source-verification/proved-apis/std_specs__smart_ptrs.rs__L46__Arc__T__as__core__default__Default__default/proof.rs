#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::sync::Arc;
use vstd::prelude::*;
use vstd::std_specs::smart_ptrs::*;

verus! {

fn source_arc_default<T: core::default::Default>() -> (res: Arc<T>)
    ensures
        T::default.ensures((), *res),
{
    // Public constructor form of the source's direct ArcInner allocation.
    let value = T::default();
    Arc::new(value)
}

} // verus!

fn main() {}