#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use vstd::prelude::*;
use vstd::std_specs::alloc::*;

verus! {

fn source_alloc_boxed_box_new_uninit<T>() -> alloc::boxed::Box<core::mem::MaybeUninit<T>>
{
    alloc::boxed::Box::new(core::mem::MaybeUninit::<T>::uninit())
}

}

fn main() {}