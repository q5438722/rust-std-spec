#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::dedup
// Source: alloc/src/vec/mod.rs:3663-3665
// Source item sha256: f9d207cd4e2bf7bc27ee990bdeed6506fd0918a24cec45d2d76f470c6a0eab96
// Dependency manifest: proof_manifests/126_alloc_vec_Vec_dedup/dependency_assumption_manifest.json
//
// The public target body below is executable and preserves the Rust 1.96
// wrapper semantics: call dedup_by with the PartialEq callback `a == b`.
// Trusted boundaries are limited to the already-reviewed dedup_by dependency
// relation and the source-backed bridge from that equality callback to the
// generated vec_dedup_partial_eq_result relation.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    ptr: *mut T,
    _marker_a: PhantomData<A>,
}

pub struct Vec<T, A: Allocator> {
    buf: RawVec<T, A>,
    len: usize,
}

pub uninterp spec fn raw_vec_initialized_seq<T, A: Allocator>(buf: &RawVec<T, A>) -> Seq<T>;

pub uninterp spec fn vec_dedup_by_result<T, F: FnMut(&mut T, &mut T) -> bool>(
    source: Seq<T>,
    same_bucket: F,
    result: Seq<T>,
) -> bool;

pub uninterp spec fn vec_dedup_partial_eq_result<T>(
    source: Seq<T>,
    result: Seq<T>,
) -> bool;

pub uninterp spec fn partial_eq_same_bucket_callback<T, F: FnMut(&mut T, &mut T) -> bool>(
    same_bucket: F,
) -> bool;

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf)
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn dedup(&mut self)
        where
            T: core::cmp::PartialEq,
        ensures
            vec_dedup_partial_eq_result(old(self)@, final(self)@),
    {
        let ghost source = self@;
        let same_bucket = |a: &mut T, b: &mut T| -> bool { a == b };
        proof {
            rust_1_96_partial_eq_callback_observation::<T, _>(same_bucket);
        }
        self.dedup_by(same_bucket);
        proof {
            rust_1_96_dedup_by_partial_eq_bridge::<T, _>(source, same_bucket, self@);
            assert(vec_dedup_partial_eq_result(old(self)@, final(self)@));
        }
    }

    #[verifier::external_body]
    pub fn dedup_by<F>(&mut self, same_bucket: F)
        where
            F: FnMut(&mut T, &mut T) -> bool,
        ensures
            vec_dedup_by_result(old(self)@, same_bucket, final(self)@),
    {
    }
}

#[verifier::external_body]
proof fn rust_1_96_partial_eq_callback_observation<T, F>(same_bucket: F)
    where
        T: core::cmp::PartialEq,
        F: FnMut(&mut T, &mut T) -> bool,
    ensures
        partial_eq_same_bucket_callback::<T, F>(same_bucket),
{
}

#[verifier::external_body]
proof fn rust_1_96_dedup_by_partial_eq_bridge<T, F>(
    source: Seq<T>,
    same_bucket: F,
    result: Seq<T>,
)
    where
        T: core::cmp::PartialEq,
        F: FnMut(&mut T, &mut T) -> bool,
    requires
        partial_eq_same_bucket_callback::<T, F>(same_bucket),
        vec_dedup_by_result(source, same_bucket, result),
    ensures
        vec_dedup_partial_eq_result(source, result),
{
}

}
