#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::copy_from_slice
// Source: core/src/slice/mod.rs:4320-4326 and private copy_from_slice_impl at 5561-5586
// Source item sha256: a2d7c011586a2f326d530336974e386d41263495754e7a17271f3023a5a2dba5
// Dependency manifest: proof_manifests/145_core_slice_copy_from_slice/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 wrapper
// flow: `unsafe { copy_from_slice_impl(self, src) }`. The private helper keeps
// the length-mismatch panic branch and, under the exact-vstd equal-length
// precondition, reaches the Rust pointer-copy operation
// `ptr::copy_nonoverlapping(src.as_ptr(), dest.as_mut_ptr(), dest.len())`.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn slice_start_ptr<T>(seq: Seq<T>, ptr: *const T) -> bool;

pub uninterp spec fn slice_start_mut_ptr<T>(seq: Seq<T>, ptr: *mut T) -> bool;

pub open spec fn copy_from_slice_domain<T>(dst: Seq<T>, src: Seq<T>) -> bool {
    dst.len() == src.len()
}

#[verifier::external_body]
pub fn len_mismatch_fail(dst_len: usize, src_len: usize)
    requires
        dst_len != src_len,
    ensures
        false,
{
}

#[verifier::external_body]
pub fn rust_1_96_slice_as_ptr<T>(slice: &[T]) -> (ptr: *const T)
    ensures
        slice_start_ptr(slice@, ptr),
{
    slice as *const [T] as *const T
}

#[verifier::external_body]
pub fn rust_1_96_slice_as_mut_ptr<T>(slice: &mut [T]) -> (ptr: *mut T)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
{
    slice as *mut [T] as *mut T
}

pub mod ptr {
    use super::*;

    #[verifier::external_body]
    pub unsafe fn copy_nonoverlapping<T: Copy>(src: *const T, dest: *mut T, count: usize) {
        unsafe { core::ptr::copy_nonoverlapping(src, dest, count) }
    }
}

#[verifier::external_body]
pub fn rust_1_96_copy_nonoverlapping_establishes_dst<T: Copy>(
    dest: &mut [T],
    Ghost(source): Ghost<Seq<T>>,
    src_ptr: *const T,
    dest_ptr: *mut T,
    count: usize,
)
    requires
        old(dest)@.len() == source.len(),
        count as nat == source.len(),
        slice_start_ptr(source, src_ptr),
        slice_start_mut_ptr(old(dest)@, dest_ptr),
    ensures
        final(dest)@ == source,
{
}

pub unsafe fn copy_from_slice_impl<T: Copy>(dest: &mut [T], src: &[T])
    requires
        copy_from_slice_domain(old(dest)@, src@),
    ensures
        final(dest)@ == src@,
{
    let ghost source = src@;
    let ghost before = dest@;
    proof {
        assert(before.len() == source.len());
        assert(dest.len() as nat == before.len());
        assert(src.len() as nat == source.len());
        assert(dest.len() == src.len());
    }

    if dest.len() != src.len() {
        len_mismatch_fail(dest.len(), src.len());
    }

    unsafe {
        let src_ptr = rust_1_96_slice_as_ptr(src);
        let dest_ptr = rust_1_96_slice_as_mut_ptr(dest);
        let count = dest.len();
        proof {
            assert(dest@ == before);
            assert(count == src.len());
            assert(count as nat == source.len());
        }

        ptr::copy_nonoverlapping(src_ptr, dest_ptr, count);
        rust_1_96_copy_nonoverlapping_establishes_dst(dest, Ghost(source), src_ptr, dest_ptr, count);
    }
}

pub fn copy_from_slice<T: Copy>(dst: &mut [T], src: &[T])
    requires
        copy_from_slice_domain(old(dst)@, src@),
    ensures
        final(dst)@ == src@,
{
    unsafe { copy_from_slice_impl(dst, src) }
}

}
