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
pub fn external_std_specs__vec_rs__l278__vec__t__a__as__clone__clone<T: Clone, A: Allocator + Clone>(
    vec: &Vec<T, A>,
) -> (res: Vec<T, A>)
    ensures
        res.len() == vec.len(),
        forall|i| #![all_triggers] 0 <= i < vec.len() ==> cloned::<T>(vec[i], res[i]),
        vec_clone_trigger(*vec, res),
        vec@ =~= res@ ==> vec@ == res@,
    { loop { } }

}

fn main() {}
