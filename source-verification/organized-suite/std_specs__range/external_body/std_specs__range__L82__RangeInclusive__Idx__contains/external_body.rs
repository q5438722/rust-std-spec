#![allow(dead_code, unused_imports, unused_variables)]
#![feature(allocator_api)]
#![feature(box_into_inner)]
#![feature(const_trait_impl)]
#![feature(exact_size_is_empty)]
#![feature(iter_advance_by)]
#![feature(layout_for_ptr)]
#![feature(maybe_uninit_as_bytes)]
#![feature(maybe_uninit_array_assume_init)]
#![feature(never_type)]
#![feature(nonzero_internals)]
#![feature(ptr_metadata)]
#![feature(slice_ptr_get)]
#![feature(sized_hierarchy)]
#![feature(step_trait)]
#![feature(trusted_len)]
#![feature(unsized_fn_params)]
extern crate alloc;
use vstd::prelude::*;
use vstd::prelude::*;
use vstd::view::View;
use vstd::std_specs::cmp::{PartialOrdIs, PartialOrdSpec};
use vstd::std_specs::iter::{IteratorSpec, StepSpec, StepSpecImpl};
use core::ops::{ Bound, Range, RangeBounds, RangeFrom, RangeFull, RangeInclusive, RangeTo, RangeToInclusive, };
use vstd::std_specs::range::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__range_rs__l82__rangeinclusive__idx__contains<Idx: PartialOrd<Idx>, U>(
    r: &RangeInclusive<Idx>,
    i: &U,
) -> (ret: bool) where Idx: PartialOrd<U>, U: ?Sized + PartialOrd<Idx>
    ensures
        <RangeInclusive::<Idx> as ContainsSpec<Idx, U>>::obeys_contains() ==> ret
            == r.contains_spec(i),
    { loop { } }

}

fn main() {}
