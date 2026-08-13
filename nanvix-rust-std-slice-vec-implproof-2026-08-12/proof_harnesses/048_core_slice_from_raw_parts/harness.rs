#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::from_raw_parts
// Source: core/src/slice/raw.rs:124-141
// Source item sha256: 9544e272f2c1f29c72893c67e1739041f27647e99198cc311eac1870c87bcfcb
// Dependency manifest: proof_manifests/048_core_slice_from_raw_parts/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost enum SliceRawMutability {
    Immutable,
    Mutable,
}

pub ghost struct SliceRawDomain {
    pub len: int,
    pub non_null: bool,
    pub aligned: bool,
    pub one_allocation: bool,
    pub initialized: bool,
    pub aliasing_ok: bool,
    pub within_isize: bool,
    pub mutability: SliceRawMutability,
}

pub uninterp spec fn slice_raw_domain<T>(
    ptr: *const T,
    len: usize,
    mutability: SliceRawMutability,
) -> SliceRawDomain;

pub open spec fn slice_raw_domain_valid(domain: SliceRawDomain) -> bool {
    0 <= domain.len
        && domain.non_null
        && domain.aligned
        && domain.one_allocation
        && domain.initialized
        && domain.aliasing_ok
        && domain.within_isize
}

pub open spec fn slice_raw_domain_valid_for(
    domain: SliceRawDomain,
    len: usize,
    mutability: SliceRawMutability,
) -> bool {
    slice_raw_domain_valid(domain) && domain.len == len as int && domain.mutability == mutability
}

pub uninterp spec fn slice_start_ptr<T>(seq: Seq<T>, ptr: *const T) -> bool;

pub open spec fn slice_from_raw_parts_result<T>(ptr: *const T, len: usize, ret: &[T]) -> bool {
    ret@.len() == len && slice_start_ptr(ret@, ptr)
}

#[verifier::external_body]
pub unsafe fn rust_1_96_from_raw_parts_ub_checked_raw_slice<'a, T>(
    data: *const T,
    len: usize,
) -> (ret: &'a [T])
    requires
        slice_raw_domain_valid_for(
            slice_raw_domain(data, len, SliceRawMutability::Immutable),
            len,
            SliceRawMutability::Immutable,
        ),
    ensures
        slice_from_raw_parts_result(data, len, ret),
{
    unsafe { &*core::ptr::slice_from_raw_parts(data, len) }
}

pub unsafe fn from_raw_parts<'a, T>(data: *const T, len: usize) -> (ret: &'a [T])
    requires
        slice_raw_domain_valid_for(
            slice_raw_domain(data, len, SliceRawMutability::Immutable),
            len,
            SliceRawMutability::Immutable,
        ),
    ensures
        slice_from_raw_parts_result(data, len, ret),
{
    unsafe { rust_1_96_from_raw_parts_ub_checked_raw_slice(data, len) }
}

}
