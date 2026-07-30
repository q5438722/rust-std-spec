#![allow(dead_code)]
#![allow(unused_imports)]

use core::mem::ManuallyDrop;
use vstd::prelude::*;
use vstd::std_specs::manually_drop::*;

verus! {

#[repr(transparent)]
pub struct MaybeDanglingRepr<T>(pub T);

impl<T> MaybeDanglingRepr<T> {
    fn new(value: T) -> (res: Self)
        ensures res.0 == value,
    {
        MaybeDanglingRepr(value)
    }
}

#[repr(transparent)]
pub struct ManuallyDropRepr<T> {
    pub value: MaybeDanglingRepr<T>,
}

}

unsafe fn manually_drop_from_rust_1_96_repr<T>(
    repr: ManuallyDropRepr<T>,
) -> ManuallyDrop<T> {
    let result = unsafe {
        core::mem::transmute_copy::<ManuallyDropRepr<T>, ManuallyDrop<T>>(&repr)
    };
    core::mem::forget(repr);
    result
}

verus! {

pub assume_specification<T>[manually_drop_from_rust_1_96_repr::<T>](
    repr: ManuallyDropRepr<T>,
) -> (res: ManuallyDrop<T>)
    ensures res@ == repr.value.0,
;

fn source_manually_drop_new<T>(value: T) -> (res: ManuallyDrop<T>)
    ensures res@ == value,
{
    let repr = ManuallyDropRepr {
        value: MaybeDanglingRepr::new(value),
    };
    unsafe { manually_drop_from_rust_1_96_repr(repr) }
}

}

fn main() {}