#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::copy_within
// Source: core/src/slice/mod.rs:4354-4370
// Source item sha256: 80a6582a6702b0a09aae49f2a9f63f1880cc44162858be6d57b095be42b8eeec
// Dependency manifest: proof_manifests/146_core_slice_copy_within/dependency_assumption_manifest.json
//
// The public target body below is executable and preserves the Rust 1.96 flow:
// slice::range, count computation, destination bounds assert, a single
// as_mut_ptr loan, ptr.add for source/destination, and overlapping ptr::copy.
// Trusted boundaries are limited to source-backed range validation, panic
// divergence, pointer provenance, and the raw overlapping-copy slice effect.

use core::marker::PhantomData;
use core::ops::{Range, RangeBounds, RangeTo};
use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub struct MutPtr<T> {
    raw: *mut T,
    _marker_t: PhantomData<T>,
}

impl<T> Copy for MutPtr<T> {
}

impl<T> Clone for MutPtr<T> {
    fn clone(&self) -> MutPtr<T> {
        MutPtr { raw: self.raw, _marker_t: PhantomData }
    }
}

pub uninterp spec fn slice_range_start<R: RangeBounds<usize>>(src: &R) -> int;

pub uninterp spec fn slice_range_end<R: RangeBounds<usize>>(src: &R, len: nat) -> int;

pub open spec fn slice_range_valid<R: RangeBounds<usize>>(src: &R, len: nat) -> bool {
    0 <= slice_range_start(src)
        && slice_range_start(src) <= slice_range_end(src, len)
        && slice_range_end(src, len) <= len
}

pub open spec fn copy_within_domain<R: RangeBounds<usize>>(
    src: &R,
    len: nat,
    dest: usize,
) -> bool {
    slice_range_valid(src, len)
        && (dest as int) + (slice_range_end(src, len) - slice_range_start(src)) <= len
}

pub open spec fn copy_within_result<T>(
    old_slice: Seq<T>,
    src_start: int,
    src_end: int,
    dest: int,
) -> Seq<T> {
    let count = src_end - src_start;
    Seq::new(
        old_slice.len(),
        |i: int|
            if dest <= i && i < dest + count {
                old_slice[src_start + (i - dest)]
            } else {
                old_slice[i]
            },
    )
}

pub uninterp spec fn slice_start_mut_ptr<T>(seq: Seq<T>, ptr: MutPtr<T>) -> bool;

pub uninterp spec fn slice_mut_ptr_add<T>(
    source: Seq<T>,
    base: MutPtr<T>,
    offset: int,
    ptr: MutPtr<T>,
) -> bool;

pub mod slice {
    use super::*;

    #[verifier::external_body]
    pub fn range<R: RangeBounds<usize>>(src: R, bounds: RangeTo<usize>) -> (ret: Range<usize>)
        requires
            slice_range_valid(&src, bounds.end as nat),
        ensures
            ret.start as int == slice_range_start(&src),
            ret.end as int == slice_range_end(&src, bounds.end as nat),
            ret.start <= ret.end,
            ret.end <= bounds.end,
    {
        0..bounds.end
    }
}

pub mod ptr {
    use super::*;

    #[verifier::external_body]
    pub unsafe fn copy<T>(src: MutPtr<T>, dest: MutPtr<T>, count: usize) {
    }
}

impl<T> MutPtr<T> {
    #[verifier::external_body]
    pub unsafe fn add(self, offset: usize) -> (ptr: MutPtr<T>)
    {
        self
    }
}

#[verifier::external_body]
pub fn rust_1_96_slice_as_mut_ptr<T>(slice: &mut [T]) -> (ptr: MutPtr<T>)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
{
    MutPtr { raw: slice as *mut [T] as *mut T, _marker_t: PhantomData }
}

#[verifier::external_body]
pub proof fn rust_1_96_mut_ptr_add_bridge<T>(
    source: Seq<T>,
    base: MutPtr<T>,
    offset: usize,
    ptr: MutPtr<T>,
)
    requires
        slice_start_mut_ptr(source, base),
        offset as nat <= source.len(),
    ensures
        slice_mut_ptr_add(source, base, offset as int, ptr),
{
}

#[verifier::external_body]
pub proof fn rust_1_96_copy_within_bounds_bridge(
    len: usize,
    src_start: usize,
    src_end: usize,
    count: usize,
    dest: usize,
    spec_src_start: int,
    spec_src_end: int,
)
    requires
        src_start as int == spec_src_start,
        src_end as int == spec_src_end,
        0 <= spec_src_start,
        spec_src_start <= spec_src_end,
        spec_src_end <= len as int,
        count as int == spec_src_end - spec_src_start,
        (dest as int) + (spec_src_end - spec_src_start) <= len as int,
    ensures
        src_start <= src_end,
        count == src_end - src_start,
        count <= len,
        dest <= len - count,
        (dest as int) + count as int <= len as int,
{
}

#[verifier::external_body]
pub fn rust_1_96_copy_within_dest_assert_failed(dest: usize, len: usize, count: usize)
    requires
        dest > len - count,
    ensures
        false,
{
}

#[verifier::external_body]
pub fn rust_1_96_overlapping_ptr_copy_establishes_slice<T>(
    slice: &mut [T],
    Ghost(source): Ghost<Seq<T>>,
    Ghost(spec_src_start): Ghost<int>,
    Ghost(spec_src_end): Ghost<int>,
    Ghost(spec_dest): Ghost<int>,
    base_ptr: MutPtr<T>,
    src_ptr: MutPtr<T>,
    dest_ptr: MutPtr<T>,
    count: usize,
)
    requires
        old(slice)@ == source,
        slice_range_valid_for_values(source.len(), spec_src_start, spec_src_end),
        spec_dest >= 0,
        spec_dest + (spec_src_end - spec_src_start) <= source.len(),
        count as int == spec_src_end - spec_src_start,
        slice_start_mut_ptr(source, base_ptr),
        slice_mut_ptr_add(source, base_ptr, spec_src_start, src_ptr),
        slice_mut_ptr_add(source, base_ptr, spec_dest, dest_ptr),
    ensures
        final(slice)@ == copy_within_result(source, spec_src_start, spec_src_end, spec_dest),
{
}

pub open spec fn slice_range_valid_for_values(len: nat, src_start: int, src_end: int) -> bool {
    0 <= src_start && src_start <= src_end && src_end <= len
}

pub fn copy_within<T: Copy, R: RangeBounds<usize>>(self_slice: &mut [T], src: R, dest: usize)
    requires
        copy_within_domain(&src, old(self_slice)@.len(), dest),
    ensures
        final(self_slice)@ == copy_within_result(
            old(self_slice)@,
            slice_range_start(&src),
            slice_range_end(&src, old(self_slice)@.len()),
            dest as int,
        ),
{
    let ghost source = self_slice@;
    let ghost spec_src_start = slice_range_start(&src);
    let ghost spec_src_end = slice_range_end(&src, source.len());
    let len = self_slice.len();
    proof {
        assert(len as nat == source.len());
        assert(slice_range_valid(&src, len as nat));
    }
    let Range { start: src_start, end: src_end } = slice::range(src, ..len);
    proof {
        assert(src_start as int == spec_src_start);
        assert(src_end as int == spec_src_end);
        assert(src_start <= src_end);
    }
    let count = src_end - src_start;
    proof {
        rust_1_96_copy_within_bounds_bridge(
            len,
            src_start,
            src_end,
            count,
            dest,
            spec_src_start,
            spec_src_end,
        );
    }
    if dest > len - count {
        rust_1_96_copy_within_dest_assert_failed(dest, len, count);
    }

    unsafe {
        let ptr = rust_1_96_slice_as_mut_ptr(self_slice);
        let src_ptr = ptr.add(src_start);
        proof {
            rust_1_96_mut_ptr_add_bridge(source, ptr, src_start, src_ptr);
        }
        let dest_ptr = ptr.add(dest);
        proof {
            rust_1_96_mut_ptr_add_bridge(source, ptr, dest, dest_ptr);
        }
        ptr::copy(src_ptr, dest_ptr, count);
        rust_1_96_overlapping_ptr_copy_establishes_slice(
            self_slice,
            Ghost(source),
            Ghost(spec_src_start),
            Ghost(spec_src_end),
            Ghost(dest as int),
            ptr,
            src_ptr,
            dest_ptr,
            count,
        );
    }
}

}
