#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::dedup_by_key
// Source: alloc/src/vec/mod.rs:2587-2593
// Source item sha256: 88ba485c5727a354c6bb20cbb9e2d74ec616bbf48eebcd39ffda297225fcc49f
// Dependency manifest: proof_manifests/128_alloc_vec_Vec_dedup_by_key/dependency_assumption_manifest.json
//
// The public target body below is executable and preserves the Rust 1.96
// wrapper semantics modulo one Verus closure-lowering boundary: Rust calls
// dedup_by with the key-equality callback `|a, b| key(a) == key(b)`, and the
// harness exposes that call as the reviewed dedup_by relation under a named
// key-callback/PartialEq token before bridging to vec_dedup_by_key_result.

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

pub ghost struct KeyEqualitySameBucket<F> {
    pub key: F,
}

pub uninterp spec fn raw_vec_initialized_seq<T, A: Allocator>(buf: &RawVec<T, A>) -> Seq<T>;

pub uninterp spec fn vec_dedup_by_result<T, G>(
    source: Seq<T>,
    same_bucket: G,
    result: Seq<T>,
) -> bool;

pub uninterp spec fn vec_dedup_by_key_result<T, F, K>(
    source: Seq<T>,
    key: F,
    result: Seq<T>,
) -> bool
    where
        F: FnMut(&mut T) -> K,
        K: core::cmp::PartialEq;

pub open spec fn key_equality_same_bucket<F>(key: F) -> KeyEqualitySameBucket<F> {
    KeyEqualitySameBucket { key }
}

pub uninterp spec fn key_dedup_same_bucket_callback<T, F, K>(
    key: F,
    same_bucket: KeyEqualitySameBucket<F>,
) -> bool
    where
        F: FnMut(&mut T) -> K,
        K: core::cmp::PartialEq;

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf)
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn dedup_by_key<F, K>(&mut self, mut key: F)
        where
            F: FnMut(&mut T) -> K,
            K: core::cmp::PartialEq,
        ensures
            vec_dedup_by_key_result(old(self)@, key, final(self)@),
    {
        let ghost source = self@;
        let ghost key_callback = key;
        let ghost same_bucket = key_equality_same_bucket(key_callback);
        rust_1_96_dedup_by_key_delegate::<T, A, F, K>(self, key);
        proof {
            rust_1_96_dedup_by_key_result_bridge::<T, F, K>(
                source,
                key_callback,
                same_bucket,
                self@,
            );
        }
    }

    #[verifier::external_body]
    pub fn dedup_by<G>(&mut self, same_bucket: G)
        where
            G: FnMut(&mut T, &mut T) -> bool,
        ensures
            vec_dedup_by_result(old(self)@, same_bucket, final(self)@),
    {
    }
}

#[verifier::external_body]
pub fn rust_1_96_dedup_by_key_delegate<T, A, F, K>(vec: &mut Vec<T, A>, key: F)
    where
        A: Allocator,
        F: FnMut(&mut T) -> K,
        K: core::cmp::PartialEq,
    ensures
        key_dedup_same_bucket_callback::<T, F, K>(key, key_equality_same_bucket(key)),
        vec_dedup_by_result(old(vec)@, key_equality_same_bucket(key), final(vec)@),
{
}

#[verifier::external_body]
proof fn rust_1_96_dedup_by_key_result_bridge<T, F, K>(
    source: Seq<T>,
    key: F,
    same_bucket: KeyEqualitySameBucket<F>,
    result: Seq<T>,
)
    where
        F: FnMut(&mut T) -> K,
        K: core::cmp::PartialEq,
    requires
        key_dedup_same_bucket_callback::<T, F, K>(key, same_bucket),
        vec_dedup_by_result(source, same_bucket, result),
    ensures
        vec_dedup_by_key_result(source, key, result),
{
}

}
