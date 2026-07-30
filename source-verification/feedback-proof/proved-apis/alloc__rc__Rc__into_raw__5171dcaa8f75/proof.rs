#![allow(dead_code)]
#![allow(unused_imports)]
#![feature(allocator_api)]

extern crate alloc;

use alloc::rc::Rc;
use core::alloc::Allocator;
use core::mem::ManuallyDrop;
use vstd::prelude::*;
use vstd::std_specs::manually_drop::*;

verus! {

pub assume_specification<T: ?Sized, A: Allocator>[ Rc::<T, A>::as_ptr ](
    this: &Rc<T, A>,
) -> (result: *const T)
    ensures
        result@.addr != 0,
;

pub fn source_rc_into_raw<T: ?Sized>(this: Rc<T>) -> (result: *const T)
    ensures
        result@.addr != 0,
{
    let this = ManuallyDrop::new(this);
    Rc::<T>::as_ptr(&*this)
}

} // verus!

fn main() {}