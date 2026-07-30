#![allow(dead_code)]
#![allow(unused_imports)]
#![feature(allocator_api)]
#![feature(sized_hierarchy)]

extern crate alloc;

use alloc::rc::Rc;
use core::alloc::Allocator;
use core::mem::ManuallyDrop;
use vstd::prelude::*;
use vstd::std_specs::manually_drop::*;
use vstd::std_specs::smart_ptrs::*;

verus! {

pub assume_specification<T: ?Sized, A: Allocator>[
    Rc::<T, A>::strong_count
](
    value: &Rc<T, A>,
) -> (count: usize);

pub assume_specification<T: ?Sized, A: Allocator>[
    Rc::<T, A>::into_raw_with_allocator
](
    value: Rc<T, A>,
) -> (parts: (*const T, A));

pub assume_specification<T: ?Sized, A: Allocator>[
    Rc::<T, A>::from_raw_in
](
    ptr: *const T,
    alloc: A,
) -> (value: Rc<T, A>);

pub uninterp spec fn spec_ptr_from_ref<V: core::marker::PointeeSized>(
    value: &V,
) -> *const V;

pub assume_specification<V: core::marker::PointeeSized>[ core::ptr::from_ref::<V> ](
    value: &V,
) -> (ptr: *const V)
    ensures
        ptr == spec_ptr_from_ref(value),
    opens_invariants none
    no_unwind
;

pub assume_specification<V>[ core::ptr::read::<V> ](
    ptr: *const V,
) -> (value: V)
    ensures
        forall|source: &V|
            ptr == spec_ptr_from_ref(source) ==> value == *source,
    opens_invariants none
    no_unwind
;

fn source_rc_try_unwrap<T, A: Allocator>(
    v: Rc<T, A>,
) -> (result: Result<T, Rc<T, A>>)
    ensures
        match result {
            Ok(t) => t == *v,
            Err(e) => e == v,
        },
{
    if Rc::strong_count(&v) == 1 {
        let this = ManuallyDrop::new(v);

        let inner: &T = &**this;
        let value_ptr = core::ptr::from_ref(inner);
        let val: T = unsafe { core::ptr::read(value_ptr) };
        assert(val == *v);

        let this = ManuallyDrop::into_inner(this);
        let (ptr, alloc) = Rc::into_raw_with_allocator(this);

        // Rebuilding the allocation with a transparent, non-dropping payload
        // performs the source's strong/implicit-weak cleanup without dropping
        // the T that was just moved out.
        let _cleanup: Rc<ManuallyDrop<T>, A> = unsafe {
            Rc::from_raw_in(ptr as *const ManuallyDrop<T>, alloc)
        };
        Ok(val)
    } else {
        Err(v)
    }
}

} // verus!

fn main() {}