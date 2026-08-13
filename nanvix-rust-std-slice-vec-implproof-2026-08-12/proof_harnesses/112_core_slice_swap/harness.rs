#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::swap
// Source: core/src/slice/mod.rs:905-917
// Source item sha256: c3f8424d1011b9a80d253d3b0b7f467d6f7a747890ca31eb841f3232d5da29da
// Dependency manifest: proof_manifests/112_core_slice_swap/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn slice_swapped<T>(seq: Seq<T>, a: int, b: int) -> Seq<T> {
    seq.update(a, seq[b]).update(b, seq[a])
}

pub uninterp spec fn slice_mut_element_ptr<T>(seq: Seq<T>, index: int, ptr: *mut T) -> bool;

#[verifier::external_body]
pub unsafe fn rust_1_96_raw_mut_element_ptr<T>(
    slice: &mut [T],
    index: usize,
) -> (ptr: *mut T)
    requires
        index < old(slice)@.len(),
    ensures
        final(slice)@ == old(slice)@,
        slice_mut_element_ptr(old(slice)@, index as int, ptr),
{
    &raw mut slice[index]
}

#[verifier::external_body]
pub unsafe fn rust_1_96_ptr_swap<T>(
    slice: &mut [T],
    pa: *mut T,
    pb: *mut T,
    a: usize,
    b: usize,
)
    requires
        a < old(slice)@.len(),
        b < old(slice)@.len(),
        slice_mut_element_ptr(old(slice)@, a as int, pa),
        slice_mut_element_ptr(old(slice)@, b as int, pb),
    ensures
        final(slice)@ == slice_swapped(old(slice)@, a as int, b as int),
{
    unsafe {
        core::ptr::swap(pa, pb);
    }
}

pub fn swap<T>(slice: &mut [T], a: usize, b: usize)
    requires
        a < old(slice)@.len(),
        b < old(slice)@.len(),
    ensures
        final(slice)@ == slice_swapped(old(slice)@, a as int, b as int),
{
    let ghost source = slice@;
    let pa = unsafe {
        rust_1_96_raw_mut_element_ptr(slice, a)
    };
    let pb = unsafe {
        rust_1_96_raw_mut_element_ptr(slice, b)
    };
    proof {
        assert(slice@ == source);
    }
    unsafe {
        rust_1_96_ptr_swap(slice, pa, pb, a, b);
    }
}

}
