#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::rc::Rc;
use vstd::prelude::*;
use vstd::std_specs::smart_ptrs::*;

verus! {

fn source_rc_default<T: core::default::Default>() -> (res: Rc<T>)
    ensures
        T::default.ensures((), *res),
{
    // Public constructor form of the source's direct RcInner allocation.
    let value = T::default();
    Rc::new(value)
}

} // verus!

fn main() {}