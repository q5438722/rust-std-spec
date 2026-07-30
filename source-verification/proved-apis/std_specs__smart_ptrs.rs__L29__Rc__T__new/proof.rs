#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::boxed::Box;
use alloc::rc::Rc;
use core::ptr::NonNull;
use vstd::prelude::*;
use vstd::std_specs::smart_ptrs::*;

verus! {

#[repr(transparent)]
pub struct UnsafeCellRepr<T> {
    pub value: T,
}

#[repr(transparent)]
pub struct CellRepr<T> {
    pub value: UnsafeCellRepr<T>,
}

fn source_unsafe_cell_new<T>(value: T) -> (res: UnsafeCellRepr<T>)
    ensures
        res.value == value,
{
    UnsafeCellRepr { value }
}

fn source_cell_new<T>(value: T) -> (res: CellRepr<T>)
    ensures
        res.value.value == value,
{
    CellRepr {
        value: source_unsafe_cell_new(value),
    }
}

#[repr(C, align(2))]
pub struct RcInnerRepr<T> {
    pub strong: CellRepr<usize>,
    pub weak: CellRepr<usize>,
    pub value: T,
}

}

unsafe fn rc_from_rust_1_96_inner<T>(inner: Box<RcInnerRepr<T>>) -> Rc<T> {
    let ptr: NonNull<RcInnerRepr<T>> = Box::leak(inner).into();
    unsafe { core::mem::transmute::<NonNull<RcInnerRepr<T>>, Rc<T>>(ptr) }
}

verus! {

pub assume_specification<T>[rc_from_rust_1_96_inner::<T>](
    inner: Box<RcInnerRepr<T>>,
) -> (res: Rc<T>)
    ensures
        *res == inner.value,
;

fn source_rc_new<T>(value: T) -> (res: Rc<T>)
    ensures
        *res == value,
{
    unsafe {
        rc_from_rust_1_96_inner(Box::new(RcInnerRepr {
            strong: source_cell_new(1),
            weak: source_cell_new(1),
            value,
        }))
    }
}

} // verus!

fn main() {}