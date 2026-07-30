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
use vstd::std_specs::cmp::{PartialEqSpec, PartialEqSpecImpl};
use vstd::std_specs::iter::IteratorSpec;
use alloc::collections::TryReserveError;
use alloc::collections::vec_deque::Iter;
use alloc::collections::vec_deque::VecDeque;
use core::alloc::Allocator;
use core::clone::Clone;
use core::ops::Index;
use core::option::Option;
use core::option::Option::None;
use vstd::std_specs::vecdeque::*;
verus! {

#[verifier::external_body]
pub fn external_std_specs__vecdeque_rs__l364__vecdeque__t__a__as__clone__clone<T: Clone, A: Allocator + Clone>(
    v: &VecDeque<T, A>,
) -> (res: VecDeque<T, A>)
    ensures
        res.len() == v.len(),
        forall|i| #![all_triggers] 0 <= i < v.len() ==> cloned::<T>(v[i], res[i]),
        vec_dequeue_clone_trigger(*v, res),
        v@ =~= res@ ==> v@ == res@,
    { loop { } }

}

fn main() {}
