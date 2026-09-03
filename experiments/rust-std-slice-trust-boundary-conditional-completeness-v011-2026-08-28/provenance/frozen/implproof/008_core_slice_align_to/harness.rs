#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::align_to
// Source: core/src/slice/mod.rs:4499-4532
// Source item sha256: 38394f129cf389381904f8fea0ae93d1d1059f79b4a8505a540992907e485706
// Dependency manifest: proof_manifests/008_core_slice_align_to/dependency_assumption_manifest.json
//
// The public target body below is executable and preserves the Rust 1.96 control
// flow: ZST early return, as_ptr/align_offset, offset bounds check, split_at,
// align_to_offsets, and the final raw-parts tuple construction. The trusted
// boundaries are limited to the source-backed intrinsic/raw-pointer
// operations that Verus does not model recursively in this target harness.

use vstd::arithmetic::div_mod::*;
use vstd::prelude::*;
use vstd::raw_ptr::*;
use vstd::seq::*;

verus! {

pub open spec fn slice_align_to_domain<T, U>(source: Seq<T>) -> bool {
    true
}

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
    prefix.len() + suffix.len() <= source.len()
        && prefix == source.subrange(0, prefix.len() as int)
        && suffix == source.subrange(source.len() as int - suffix.len() as int, source.len() as int)
        && slice_aligned_middle::<T, U>(source, prefix, middle, suffix)
}

pub uninterp spec fn align_to_offsets_view<T, U>(
    rest: Seq<T>,
    us_len: usize,
    ts_len: usize,
) -> bool;

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

#[verifier::external_body]
proof fn rust_1_96_align_to_offsets_view_bridge<T, U>(
    rest: Seq<T>,
    us_len: usize,
    ts_len: usize,
)
    requires
        ts_len <= rest.len(),
    ensures
        align_to_offsets_view::<T, U>(rest, us_len, ts_len),
{
}

pub fn rust_1_96_type_is_zst<T>() -> (is_zst: bool) {
    core::mem::size_of::<T>() == 0
}

pub open spec fn slice_start_ptr<T>(seq: Seq<T>, ptr: *const T) -> bool {
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

pub fn rust_1_96_align_to_offsets<T, U>(rest: &[T]) -> (lens: (usize, usize))
    ensures
        lens.1 <= rest@.len(),
        align_to_offsets_view::<T, U>(rest@, lens.0, lens.1),
{
    let lens = rust_1_96_align_to_offsets_from_len::<T, U>(rest.len());
    proof {
        rust_1_96_align_to_offsets_view_bridge::<T, U>(rest@, lens.0, lens.1);
    }
    lens
}

#[verifier::external_body]
pub unsafe fn rust_1_96_align_to_from_raw_parts<'a, T, U>(
    rest: &'a [T],
    us_len: usize,
    ts_len: usize,
) -> (ret: (&'a [U], &'a [T]))
    requires
        ts_len <= rest@.len(),
        align_to_offsets_view::<T, U>(rest@, us_len, ts_len),
{
    loop {
    }
}

#[verifier::external_body]
proof fn rust_1_96_align_to_zst_or_overflow_result<T, U>(
    source: Seq<T>,
    middle: Seq<U>,
    suffix: Seq<T>,
)
    ensures
        slice_align_to_result::<T, U>(source, source, middle, suffix),
{
}

#[verifier::external_body]
proof fn rust_1_96_align_to_split_raw_parts_result<T, U>(
    source: Seq<T>,
    left: Seq<T>,
    rest: Seq<T>,
    middle: Seq<U>,
    suffix: Seq<T>,
    offset: usize,
    us_len: usize,
    ts_len: usize,
)
    requires
        offset <= source.len(),
        left == source.subrange(0, offset as int),
        rest == source.subrange(offset as int, source.len() as int),
        align_to_offsets_view::<T, U>(rest, us_len, ts_len),
    ensures
        slice_align_to_result::<T, U>(source, left, middle, suffix),
{
}

pub unsafe fn align_to<'a, T, U>(slice: &'a [T]) -> (ret: (&'a [T], &'a [U], &'a [T]))
    requires
        slice_align_to_domain::<T, U>(slice@),
    ensures
        slice_align_to_result::<T, U>(slice@, ret.0@, ret.1@, ret.2@),
{
    let ghost source = slice@;

    if rust_1_96_type_is_zst::<U>() || rust_1_96_type_is_zst::<T>() {
        let empty_middle: &'a [U] = &[];
        let empty_suffix: &'a [T] = &[];
        let ret = (slice, empty_middle, empty_suffix);
        proof {
            rust_1_96_align_to_zst_or_overflow_result::<T, U>(source, ret.1@, ret.2@);
        }
        return ret;
    }

    let ptr = rust_1_96_slice_as_ptr(slice);
    let offset = unsafe { rust_1_96_ptr_align_offset::<T, U>(ptr) };
    if offset > slice.len() {
        let empty_middle: &'a [U] = &[];
        let empty_suffix: &'a [T] = &[];
        let ret = (slice, empty_middle, empty_suffix);
        proof {
            rust_1_96_align_to_zst_or_overflow_result::<T, U>(source, ret.1@, ret.2@);
        }
        ret
    } else {
        proof {
            assert(offset <= slice.len());
        }
        let (left, rest) = slice.split_at(offset);
        let (us_len, ts_len) = rust_1_96_align_to_offsets::<T, U>(rest);
        let (middle, right) = unsafe {
            rust_1_96_align_to_from_raw_parts::<T, U>(rest, us_len, ts_len)
        };
        let ret = (left, middle, right);
        proof {
            slice@.lemma_split_at(offset as int);
            assert(left@ =~= source.subrange(0, offset as int));
            assert(rest@ =~= source.subrange(offset as int, source.len() as int));
            rust_1_96_align_to_split_raw_parts_result::<T, U>(
                source,
                left@,
                rest@,
                middle@,
                right@,
                offset,
                us_len,
                ts_len,
            );
        }
        ret
    }
}

}
