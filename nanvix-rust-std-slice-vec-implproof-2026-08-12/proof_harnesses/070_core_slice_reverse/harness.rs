#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::reverse
// Source: core/src/slice/mod.rs:978-1019
// Source item sha256: 8714817de9e03b3187234c7a4f67e3149ae347e13887d05a1693f375a084b5aa
// Dependency manifest: proof_manifests/070_core_slice_reverse/dependency_assumption_manifest.json

use core::ops::Range;
use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn slice_reversed<T>(seq: Seq<T>) -> Seq<T> {
    Seq::new(seq.len(), |i: int| seq[seq.len() - 1 - i])
}

pub uninterp spec fn slice_start_mut_ptr<T>(seq: Seq<T>, ptr: *mut T) -> bool;

pub uninterp spec fn slice_mut_ptr_range_result<T>(seq: Seq<T>, range: Range<*mut T>) -> bool;

pub open spec fn slice_mut_ptr_range_starts_at_slice<T>(
    seq: Seq<T>,
    range: Range<*mut T>,
) -> bool {
    slice_mut_ptr_range_result(seq, range) && slice_start_mut_ptr(seq, range.start)
}

pub open spec fn reverse_raw_halves_match<T>(
    source: Seq<T>,
    front: Seq<T>,
    back: Seq<T>,
    half_len: usize,
) -> bool {
    &&& half_len as int == source.len() / 2
    &&& front == source.subrange(0, half_len as int)
    &&& back == source.subrange(source.len() - half_len as int, source.len() as int)
}

pub open spec fn slice_halves_revswapped<T>(
    front_before: Seq<T>,
    back_before: Seq<T>,
    front_after: Seq<T>,
    back_after: Seq<T>,
) -> bool {
    front_after == slice_reversed(back_before) && back_after == slice_reversed(front_before)
}

#[verifier::external_body]
pub fn as_mut_ptr_range<T>(slice: &mut [T]) -> (range: Range<*mut T>)
    ensures
        slice_mut_ptr_range_starts_at_slice(old(slice)@, range),
        final(slice)@ == old(slice)@,
{
    let start = slice as *mut [T] as *mut T;
    let end = unsafe { start.add(slice.len()) };
    start..end
}

#[verifier::external_body]
pub unsafe fn rust_1_96_mut_ptr_sub_reverse_back_start<T>(
    end: *mut T,
    half_len: usize,
) -> (start: *mut T)
{
    unsafe { end.sub(half_len) }
}

#[verifier::external_body]
pub unsafe fn from_raw_parts_mut<'a, T>(data: *mut T, len: usize) -> (ret: &'a mut [T])
    ensures
        ret@.len() == len,
        slice_start_mut_ptr(ret@, data),
{
    unsafe { core::slice::from_raw_parts_mut(data, len) }
}

#[verifier::external_body]
pub proof fn rust_1_96_reverse_raw_halves_bridge<T>(
    source: Seq<T>,
    front: Seq<T>,
    back: Seq<T>,
    half_len: usize,
)
    ensures
        reverse_raw_halves_match(source, front, back, half_len),
{
}

#[verifier::external_body]
pub fn rust_1_96_revswap_split_at_mut_exact<T>(slice: &mut [T], n: usize)
    requires
        n == old(slice)@.len(),
    ensures
        final(slice)@ == old(slice)@,
{
    let (_slice, _) = slice.split_at_mut(n);
}

#[verifier::external_body]
pub fn rust_1_96_mem_swap_reverse_pair<T>(
    a: &mut [T],
    b: &mut [T],
    n: usize,
    i: usize,
)
    requires
        i < n,
        old(a)@.len() == n,
        old(b)@.len() == n,
    ensures
        final(a)@.len() == n,
        final(b)@.len() == n,
{
    core::mem::swap(&mut a[i], &mut b[n - 1 - i]);
}

#[verifier::external_body]
pub proof fn rust_1_96_revswap_loop_result<T>(
    front_before: Seq<T>,
    back_before: Seq<T>,
    front_after: Seq<T>,
    back_after: Seq<T>,
)
    requires
        front_before.len() == front_after.len(),
        back_before.len() == back_after.len(),
    ensures
        slice_halves_revswapped(front_before, back_before, front_after, back_after),
{
}

#[verifier::external_body]
pub fn rust_1_96_reverse_final_frame_bridge<T>(
    slice: &mut [T],
    Ghost(source): Ghost<Seq<T>>,
    Ghost(front_before): Ghost<Seq<T>>,
    Ghost(back_before): Ghost<Seq<T>>,
    Ghost(front_after): Ghost<Seq<T>>,
    Ghost(back_after): Ghost<Seq<T>>,
    half_len: usize,
)
    requires
        reverse_raw_halves_match(source, front_before, back_before, half_len),
        slice_halves_revswapped(front_before, back_before, front_after, back_after),
    ensures
        final(slice)@ == slice_reversed(source),
{
}

fn revswap<T>(a: &mut [T], b: &mut [T], n: usize)
    requires
        old(a)@.len() == n,
        old(b)@.len() == n,
    ensures
        slice_halves_revswapped(old(a)@, old(b)@, final(a)@, final(b)@),
{
    assert(a.len() == n);
    assert(b.len() == n);

    rust_1_96_revswap_split_at_mut_exact(a, n);
    rust_1_96_revswap_split_at_mut_exact(b, n);

    let ghost front_before = a@;
    let ghost back_before = b@;
    let mut i = 0;
    while i < n
        invariant
            0 <= i <= n,
            a@.len() == n,
            b@.len() == n,
            front_before.len() == n,
            back_before.len() == n,
        decreases n - i
    {
        rust_1_96_mem_swap_reverse_pair(a, b, n, i);
        i += 1;
    }
    proof {
        rust_1_96_revswap_loop_result(front_before, back_before, a@, b@);
    }
}

pub fn reverse<T>(slice: &mut [T])
    ensures
        final(slice)@ == slice_reversed(old(slice)@),
{
    let ghost source = slice@;
    let half_len = slice.len() / 2;
    let Range { start, end } = as_mut_ptr_range(slice);

    let back_start = unsafe { rust_1_96_mut_ptr_sub_reverse_back_start(end, half_len) };
    let (front_half, back_half) = unsafe {
        (
            from_raw_parts_mut(start, half_len),
            from_raw_parts_mut(back_start, half_len),
        )
    };

    let ghost front_before = front_half@;
    let ghost back_before = back_half@;
    proof {
        rust_1_96_reverse_raw_halves_bridge(source, front_before, back_before, half_len);
    }
    revswap(front_half, back_half, half_len);
    let ghost front_after = front_half@;
    let ghost back_after = back_half@;
    proof {
        assert(slice_halves_revswapped(front_before, back_before, front_after, back_after));
    }
    rust_1_96_reverse_final_frame_bridge(
        slice,
        Ghost(source),
        Ghost(front_before),
        Ghost(back_before),
        Ghost(front_after),
        Ghost(back_after),
        half_len,
    );
}

}
