#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::from_raw_parts_mut
// Source: core/src/slice/raw.rs:179-196
// Source item sha256: b19fba4b6bde2fc2195bda8acded38ced9f42f1eb67c475260a1e84a9c667093
// Dependency manifest: proof_manifests/049_core_slice_from_raw_parts_mut/dependency_assumption_manifest.json

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

pub uninterp spec fn slice_raw_mut_domain<T>(
    ptr: *mut T,
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

pub uninterp spec fn slice_start_mut_ptr<T>(seq: Seq<T>, ptr: *mut T) -> bool;

pub open spec fn slice_from_raw_parts_mut_result<T>(
    ptr: *mut T,
    len: usize,
    ret: &mut [T],
) -> bool {
    ret@.len() == len && slice_start_mut_ptr(ret@, ptr)
}

#[verifier::external_body]
pub unsafe fn rust_1_96_from_raw_parts_mut_ub_checked_raw_slice<'a, T>(
    data: *mut T,
    len: usize,
) -> (ret: &'a mut [T])
    requires
        slice_raw_domain_valid_for(
            slice_raw_mut_domain(data, len, SliceRawMutability::Mutable),
            len,
            SliceRawMutability::Mutable,
        ),
    ensures
        slice_from_raw_parts_mut_result(data, len, ret),
{
    unsafe { &mut *core::ptr::slice_from_raw_parts_mut(data, len) }
}

pub unsafe fn from_raw_parts_mut<'a, T>(data: *mut T, len: usize) -> (ret: &'a mut [T])
    requires
        slice_raw_domain_valid_for(
            slice_raw_mut_domain(data, len, SliceRawMutability::Mutable),
            len,
            SliceRawMutability::Mutable,
        ),
    ensures
        slice_from_raw_parts_mut_result(data, len, ret),
{
    unsafe { rust_1_96_from_raw_parts_mut_ub_checked_raw_slice(data, len) }
}

}
