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
use vstd::seq::*;
use vstd::slice::SliceAdditionalSpecFns;
use vstd::std_specs::iter::IteratorSpec;
use vstd::view::*;
use vstd::array::*;
verus! {

#[verifier::external_body]
pub fn external_array_rs__l120__a__t__n__as__core__iter__intoiterator__into_iter<
    'a,
    T,
    const N: usize,
>(s: &'a [T; N]) -> (iter: core::slice::Iter<
    'a,
    T,
>)
    ensures
        iter == spec_array_iter(s),
        IteratorSpec::decrease(&iter) is Some,
        IteratorSpec::initial_value_relation(&iter, &iter),
    { loop { } }

}

fn main() {}
