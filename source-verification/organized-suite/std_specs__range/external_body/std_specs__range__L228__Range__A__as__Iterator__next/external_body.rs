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
pub fn external_std_specs__range_rs__l228__range__a__as__iterator__next<A: core::iter::Step>(
    range: &mut Range<A>,
) -> (r: Option<A>)
    ensures
        (*final(range), r) == spec_range_next(*old(range)),
    { loop { } }

}

fn main() {}
