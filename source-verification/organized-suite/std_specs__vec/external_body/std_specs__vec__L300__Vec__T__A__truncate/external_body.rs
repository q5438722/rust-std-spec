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
use vstd::std_specs::iter::{FromIteratorSpecImpl, IteratorSpec};
use verus_builtin::*;
use vstd::slice::SliceIndexSpec;
use vstd::std_specs::core::IndexSpec;
use alloc::collections::TryReserveError;
use alloc::vec::{IntoIter, Vec};
use core::alloc::Allocator;
use core::clone::Clone;
use core::marker::PhantomData;
use core::ops::Index;
use core::option::Option;
use core::option::Option::None;
use core::slice::SliceIndex;
use vstd::std_specs::vec::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__vec_rs__l300__vec__t__a__truncate<T, A: Allocator>(vec: &mut Vec<T, A>, len: usize)
    ensures
        len <= old(vec).len() ==> final(vec)@ == old(vec)@.subrange(0, len as int),
        len > old(vec).len() ==> final(vec)@ == old(vec)@,
    { loop { } }

}

fn main() {}
