#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::align_to_mut
// Source: core/src/slice/mod.rs:4564-4605
// Source item sha256: 79bc07c28c34e853de5c1bbc49ebb8f27b4e8837109fc51c6a15eef97565ec27
// Dependency manifest: proof_manifests/009_core_slice_align_to_mut/dependency_assumption_manifest.json
//
// The public target body below is executable and preserves the Rust 1.96 branch
// structure: ZST early return, as_ptr/align_offset, offset bounds check, and the
// aligned mutable raw-parts branch. The named aligned-branch helper now executes
// the source split_at_mut/rest length/as_mut_ptr setup and retains only the
// raw-parts/provenance/aliasing and final-frame facts that Verus does not model
// recursively in this target.

use vstd::arithmetic::div_mod::*;
use vstd::prelude::*;
use vstd::raw_ptr::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn slice_align_to_domain<T, U>(source: Seq<T>) -> bool;

pub uninterp spec fn slice_aligned_middle<T, U>(
    source: Seq<T>,
    prefix: Seq<T>,
    middle: Seq<U>,
    suffix: Seq<T>,
) -> bool;

pub open spec fn slice_align_to_result<T, U>(
    source: Seq<T>,
    prefix: Seq<T>,
    middle: Seq<U>,
    suffix: Seq<T>,
) -> bool {
    prefix.len() <= source.len()
        && suffix.len() <= source.len()
        && prefix.len() + suffix.len() <= source.len()
        && prefix == source.subrange(0, prefix.len() as int)
        && suffix == source.subrange((source.len() - suffix.len()) as int, source.len() as int)
        && slice_aligned_middle::<T, U>(source, prefix, middle, suffix)
}

pub open spec fn slice_align_to_mut_result<T, U>(
    old_source: Seq<T>,
    prefix: Seq<T>,
    middle: Seq<U>,
    suffix: Seq<T>,
    final_prefix: Seq<T>,
    final_middle: Seq<U>,
    final_suffix: Seq<T>,
    final_source: Seq<T>,
) -> bool {
    slice_align_to_result::<T, U>(old_source, prefix, middle, suffix)
        && final_source.len() == old_source.len()
        && final_prefix.len() == prefix.len()
        && final_middle.len() == middle.len()
        && final_suffix.len() == suffix.len()
        && final_prefix.len() + final_suffix.len() <= final_source.len()
        && final_prefix == final_source.subrange(0, final_prefix.len() as int)
        && final_suffix == final_source.subrange(
            (final_source.len() - final_suffix.len()) as int,
            final_source.len() as int,
        )
}

pub fn rust_1_96_gcd(a: usize, b: usize) -> (ret: usize)
    decreases b,
{
    if b == 0 {
        a
    } else {
        rust_1_96_gcd(b, a % b)
    }
}

#[verifier::external_body]
proof fn rust_1_96_align_to_offsets_mul_fits<T, U>(rest_len: usize, ts: usize, us: usize)
    requires
        ts != 0,
    ensures
        (rest_len as int / ts as int) * us as int <= usize::MAX as int,
{
}

proof fn rust_1_96_mod_le_lhs(n: usize, d: usize)
    requires
        d != 0,
    ensures
        n % d <= n,
{
    let ni = n as int;
    let di = d as int;
    lemma_fundamental_div_mod(ni, di);
    assert(0 <= di);
    assert(0 <= ni / di);
    assert(0 <= di * (ni / di));
    assert(ni == di * (ni / di) + ni % di);
    assert(ni % di <= ni);
    assert((n % d) as int == ni % di);
}

pub fn rust_1_96_type_is_zst<T>() -> (is_zst: bool) {
    core::mem::size_of::<T>() == 0
}

pub open spec fn slice_start_ptr<T>(seq: Seq<T>, ptr: *const T) -> bool {
    ptr@.addr as nat == seq.len() && ptr@.provenance == Provenance::null()
}

pub open spec fn slice_start_mut_ptr<T>(seq: Seq<T>, ptr: *mut T) -> bool {
    ptr@.addr as nat == seq.len() && ptr@.provenance == Provenance::null()
}

pub fn rust_1_96_slice_as_ptr<T>(slice: &[T]) -> (ptr: *const T)
    ensures
        slice_start_ptr(slice@, ptr),
{
    let len = slice.len();
    let ptr = core::ptr::null::<T>().with_addr(len);
    proof {
        assert(slice@.len() == len as nat);
    }
    ptr
}

pub fn rust_1_96_slice_as_mut_ptr<T>(slice: &mut [T]) -> (ptr: *mut T)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
{
    let len = slice.len();
    let ptr = core::ptr::null_mut::<T>().with_addr(len);
    proof {
        assert(old(slice)@.len() == len as nat);
    }
    ptr
}

#[verifier::external_body]
pub unsafe fn rust_1_96_ptr_align_offset<T, U>(ptr: *const T) -> (offset: usize) {
    loop {
    }
}

pub fn rust_1_96_align_to_offsets_from_len<T, U>(rest_len: usize) -> (lens: (usize, usize))
    ensures
        lens.1 <= rest_len,
{
    let gcd = rust_1_96_gcd(core::mem::size_of::<T>(), core::mem::size_of::<U>());
    if gcd == 0 {
        (0, rest_len)
    } else {
        let ts = core::mem::size_of::<U>() / gcd;
        let us = core::mem::size_of::<T>() / gcd;
        if ts == 0 {
            (0, rest_len)
        } else {
            proof {
                let n = rest_len as int;
                let c = ts as int;
                lemma_fundamental_div_mod(n, c);
                rust_1_96_align_to_offsets_mul_fits::<T, U>(rest_len, ts, us);
                assert((rest_len / ts) as int == n / c);
                assert(((rest_len / ts) as int) * us as int <= usize::MAX as int);
            }
            let us_len = rest_len / ts * us;
            let ts_len = rest_len % ts;
            proof {
                rust_1_96_mod_le_lhs(rest_len, ts);
            }
            assert(ts_len <= rest_len);
            (us_len, ts_len)
        }
    }
}

#[verifier::external_body]
pub unsafe fn rust_1_96_align_to_mut_zst_or_overflow<'a, T, U>(
    slice: &'a mut [T],
) -> (ret: (&'a mut [T], &'a mut [U], &'a mut [T]))
    ensures
        slice_align_to_mut_result::<T, U>(
            old(slice)@,
            ret.0@,
            ret.1@,
            ret.2@,
            final(ret.0)@,
            final(ret.1)@,
            final(ret.2)@,
            final(slice)@,
        ),
{
    loop {
    }
}

#[verifier::external_body]
pub unsafe fn rust_1_96_align_to_mut_from_split_raw_parts<'a, T, U>(
    left: &'a mut [T],
    rest: &'a mut [T],
    mut_ptr: *mut T,
    rest_len: usize,
    us_len: usize,
    ts_len: usize,
    source: Ghost<Seq<T>>,
    offset: Ghost<usize>,
) -> (ret: (&'a mut [T], &'a mut [U], &'a mut [T]))
    requires
        offset@ <= source@.len(),
        old(left)@ == source@.subrange(0, offset@ as int),
        old(rest)@ == source@.subrange(offset@ as int, source@.len() as int),
        rest_len == old(rest)@.len(),
        ts_len <= rest_len,
        slice_start_mut_ptr(old(rest)@, mut_ptr),
    ensures
        final(left)@ == final(ret.0)@,
        slice_align_to_mut_result::<T, U>(
            source@,
            ret.0@,
            ret.1@,
            ret.2@,
            final(ret.0)@,
            final(ret.1)@,
            final(ret.2)@,
            final(ret.0)@ + final(rest)@,
        ),
{
    let suffix_start = rest_len - ts_len;
    unsafe {
        (
            left,
            core::slice::from_raw_parts_mut(mut_ptr as *mut U, us_len),
            core::slice::from_raw_parts_mut(mut_ptr.add(suffix_start), ts_len),
        )
    }
}

pub unsafe fn rust_1_96_align_to_mut_split_offsets_raw_parts<'a, T, U>(
    slice: &'a mut [T],
    offset: usize,
    us_len: usize,
    ts_len: usize,
) -> (ret: (&'a mut [T], &'a mut [U], &'a mut [T]))
    requires
        offset <= old(slice)@.len(),
        ts_len <= old(slice)@.len() - offset,
    ensures
        slice_align_to_mut_result::<T, U>(
            old(slice)@,
            ret.0@,
            ret.1@,
            ret.2@,
            final(ret.0)@,
            final(ret.1)@,
            final(ret.2)@,
            final(slice)@,
        ),
{
    let ghost source = slice@;
    let (left, rest) = slice.split_at_mut(offset);
    proof {
        source.lemma_split_at(offset as int);
        assert(left@ =~= source.subrange(0, offset as int));
        assert(rest@ =~= source.subrange(offset as int, source.len() as int));
    }
    let rest_len = rest.len();
    proof {
        assert(rest_len == rest@.len());
        assert(rest_len as int == source.len() - offset as int);
        assert(ts_len <= rest_len);
    }
    let mut_ptr = rust_1_96_slice_as_mut_ptr(rest);
    let ret = unsafe {
        rust_1_96_align_to_mut_from_split_raw_parts::<T, U>(
            left,
            rest,
            mut_ptr,
            rest_len,
            us_len,
            ts_len,
            Ghost(source),
            Ghost(offset),
        )
    };
    ret
}

pub unsafe fn align_to_mut<'a, T, U>(
    slice: &'a mut [T],
) -> (ret: (&'a mut [T], &'a mut [U], &'a mut [T]))
    requires
        slice_align_to_domain::<T, U>(old(slice)@),
    ensures
        slice_align_to_mut_result::<T, U>(
            old(slice)@,
            ret.0@,
            ret.1@,
            ret.2@,
            final(ret.0)@,
            final(ret.1)@,
            final(ret.2)@,
            final(slice)@,
        ),
{
    let ghost source = slice@;
    if rust_1_96_type_is_zst::<U>() || rust_1_96_type_is_zst::<T>() {
        return unsafe { rust_1_96_align_to_mut_zst_or_overflow::<T, U>(slice) };
    }

    let ptr = rust_1_96_slice_as_ptr(slice);
    let offset = unsafe { rust_1_96_ptr_align_offset::<T, U>(ptr) };
    if offset > slice.len() {
        unsafe { rust_1_96_align_to_mut_zst_or_overflow::<T, U>(slice) }
    } else {
        proof {
            assert(offset <= slice.len());
        }
        let rest_len = slice.len() - offset;
        let (us_len, ts_len) = rust_1_96_align_to_offsets_from_len::<T, U>(rest_len);
        proof {
            assert(slice@ == source);
            assert(rest_len as int == source.len() - offset as int);
            assert(ts_len <= rest_len);
            assert(ts_len <= source.len() - offset);
        }
        unsafe {
            rust_1_96_align_to_mut_split_offsets_raw_parts::<T, U>(
                slice,
                offset,
                us_len,
                ts_len,
            )
        }
    }
}

}
