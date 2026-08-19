#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::len
// Source: alloc/src/vec/mod.rs:3022-3031
// Source item sha256: 9a5623f9b76cb14b0b28093628349266c82b8ea1f53fdd88fffe49ad6cd1ceaf
// Dependency manifest: proof_manifests/165_alloc_vec_Vec_len/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// `let len = self.len; unsafe { intrinsics::assume(len <= T::MAX_SLICE_LEN) }; len`.
// The optimization hint is lowered to an executable no-effect helper; the exact
// existing-vstd contract remains `len == spec_vec_len(vec)`.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    _marker_t: PhantomData<T>,
    _marker_a: PhantomData<A>,
}

pub struct Vec<T, A: Allocator> {
    buf: RawVec<T, A>,
    len: usize,
}

pub uninterp spec fn raw_vec_value<T, A: Allocator>(buf: &RawVec<T, A>, i: int) -> T;

pub open spec fn raw_vec_initialized_seq<T, A: Allocator>(
    buf: &RawVec<T, A>,
    len: usize,
) -> Seq<T> {
    Seq::new(len as nat, |i: int| raw_vec_value(buf, i))
}

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf, self.len)
    }
}

pub uninterp spec fn spec_vec_len<T, A: Allocator>(vec: &Vec<T, A>) -> usize;

pub broadcast axiom fn axiom_spec_len<T, A: Allocator>(vec: &Vec<T, A>)
    ensures
        #[trigger] spec_vec_len(vec) == vec@.len(),
;

impl<T, A: Allocator> Vec<T, A> {
    unsafe fn rust_1_96_intrinsics_assume_len_le_max_slice_len(len: usize) {
        let _ = len;
    }

    pub fn len(&self) -> (len: usize)
        ensures
            len == spec_vec_len(self),
    {
        let len = self.len;
        unsafe {
            Self::rust_1_96_intrinsics_assume_len_le_max_slice_len(len);
        }
        proof {
            axiom_spec_len(self);
        }
        len
    }
}

}
