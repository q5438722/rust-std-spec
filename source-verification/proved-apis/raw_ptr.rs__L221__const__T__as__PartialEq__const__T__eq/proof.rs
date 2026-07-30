#![feature(ptr_metadata, sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::raw_ptr::*;

verus! {

pub assume_specification<V: core::marker::PointeeSized>[ core::ptr::metadata::<V> ](
    ptr: *const V,
) -> (metadata: <V as core::ptr::Pointee>::Metadata)
    ensures
        metadata == ptr@.metadata,
    opens_invariants none
    no_unwind
;

pub axiom fn axiom_pointee_metadata_eq<T: core::marker::PointeeSized>()
    ensures
        <<T as core::ptr::Pointee>::Metadata as vstd::std_specs::cmp::PartialEqSpec>::obeys_eq_spec(),
        forall|x: <T as core::ptr::Pointee>::Metadata,
               y: <T as core::ptr::Pointee>::Metadata|
            <<T as core::ptr::Pointee>::Metadata as vstd::std_specs::cmp::PartialEqSpec>::eq_spec(
                &x,
                &y,
            ) <==> x == y,
;

fn source_const_ptr_eq<T: core::marker::PointeeSized>(
    x: &*const T,
    y: &*const T,
) -> (res: bool)
    ensures
        res <==> (x@.addr == y@.addr) && (x@.metadata == y@.metadata),
{
    proof {
        axiom_pointee_metadata_eq::<T>();
    }
    ((*x).addr() == (*y).addr())
        && (core::ptr::metadata(*x) == core::ptr::metadata(*y))
}

}

fn main() {}