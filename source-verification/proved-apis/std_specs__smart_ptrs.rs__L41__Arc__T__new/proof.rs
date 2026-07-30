#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::boxed::Box;
use alloc::sync::Arc;
use core::sync::atomic;
use vstd::prelude::*;
use vstd::std_specs::smart_ptrs::*;

verus! {

// Mirror of Rust 1.96's private alloc::sync::ArcInner<T>.
#[repr(C, align(2))]
pub struct ArcInnerRepr<T> {
    pub strong: atomic::AtomicUsize,
    pub weak: atomic::AtomicUsize,
    pub data: T,
}

}

unsafe fn arc_from_rust_1_96_inner<T>(inner: Box<ArcInnerRepr<T>>) -> Arc<T> {
    let inner = Box::leak(inner);
    unsafe { Arc::from_raw(core::ptr::addr_of!(inner.data)) }
}

verus! {

pub assume_specification<T>[arc_from_rust_1_96_inner::<T>](
    inner: Box<ArcInnerRepr<T>>,
) -> (res: Arc<T>)
    ensures
        *res == inner.data,
;

fn source_arc_new<T>(data: T) -> (res: Arc<T>)
    ensures
        *res == data,
{
    // Start the weak pointer count as 1 which is the weak pointer that's
    // held by all the strong pointers.
    let x: Box<_> = Box::new(ArcInnerRepr {
        strong: atomic::AtomicUsize::new(1),
        weak: atomic::AtomicUsize::new(1),
        data,
    });
    unsafe { arc_from_rust_1_96_inner(x) }
}

} // verus!

fn main() {}