#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::retain
// Source: alloc/src/vec/mod.rs:2451-2456
// Source item sha256: 540fdc2fe9d77c2299dfdb8c7c4cd4cead9183e95cba156f4ee96908d4dc3223
// Dependency manifest: proof_manifests/141_alloc_vec_Vec_retain/dependency_assumption_manifest.json
//
// The public target body below is executable and preserves the Rust 1.96
// wrapper semantics modulo one Verus closure-lowering boundary: Rust calls
// retain_mut with `|elem| f(elem)`, and the harness exposes that call as the
// reviewed retain_mut relation under a named read-only-to-mutable callback
// token before bridging to vec_retain_result.

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

pub ghost struct RetainReadonlyAsMutPredicate<F> {
    pub f: F,
}

pub uninterp spec fn vec_retain_mut_result<T, G>(
    source: Seq<T>,
    predicate: G,
    result: Seq<T>,
) -> bool;

pub uninterp spec fn vec_retain_result<T, F: FnMut(&T) -> bool>(
    source: Seq<T>,
    f: F,
    result: Seq<T>,
) -> bool;

pub open spec fn retain_readonly_as_mut_predicate<F>(f: F) -> RetainReadonlyAsMutPredicate<F> {
    RetainReadonlyAsMutPredicate { f }
}

pub uninterp spec fn retain_readonly_as_mut_callback<T, F>(
    f: F,
    predicate: RetainReadonlyAsMutPredicate<F>,
) -> bool
    where
        F: FnMut(&T) -> bool;

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf)
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn retain<F>(&mut self, mut f: F)
        where
            F: FnMut(&T) -> bool,
        ensures
            vec_retain_result(old(self)@, f, final(self)@),
    {
        let ghost source = self@;
        let ghost callback = f;
        let ghost retain_predicate = retain_readonly_as_mut_predicate(callback);
        rust_1_96_retain_delegate::<T, A, F>(self, f);
        proof {
            rust_1_96_retain_result_bridge::<T, F>(
                source,
                callback,
                retain_predicate,
                self@,
            );
        }
    }

    #[verifier::external_body]
    pub fn retain_mut<G>(&mut self, predicate: G)
        where
            G: FnMut(&mut T) -> bool,
        ensures
            vec_retain_mut_result(old(self)@, predicate, final(self)@),
    {
    }
}

#[verifier::external_body]
pub fn rust_1_96_retain_delegate<T, A, F>(vec: &mut Vec<T, A>, f: F)
    where
        A: Allocator,
        F: FnMut(&T) -> bool,
    ensures
        retain_readonly_as_mut_callback::<T, F>(f, retain_readonly_as_mut_predicate(f)),
        vec_retain_mut_result(
            old(vec)@,
            retain_readonly_as_mut_predicate(f),
            final(vec)@,
        ),
{
}

#[verifier::external_body]
proof fn rust_1_96_retain_result_bridge<T, F>(
    source: Seq<T>,
    f: F,
    predicate: RetainReadonlyAsMutPredicate<F>,
    result: Seq<T>,
)
    where
        F: FnMut(&T) -> bool,
    requires
        retain_readonly_as_mut_callback::<T, F>(f, predicate),
        vec_retain_mut_result(source, predicate, result),
    ensures
        vec_retain_result(source, f, result),
{
}

}
