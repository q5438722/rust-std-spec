#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::eq_ignore_ascii_case
// Source: core/src/slice/ascii.rs:60-78 and private helpers at lines 83-159
// Source item sha256: c59a44eedf5be63e0c717c033a34687626e0746f84f17df116753330e0d70b1d
// Dependency manifest: proof_manifests/041_core_slice_eq_ignore_ascii_case/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn ascii_is_uppercase(byte: u8) -> bool {
    0x41 <= (byte as int) && (byte as int) <= 0x5a
}

pub open spec fn ascii_lower_byte(byte: u8) -> u8 {
    if ascii_is_uppercase(byte) {
        ((byte as int) + 0x20) as u8
    } else {
        byte
    }
}

pub open spec fn ascii_eq_ignore_case(left: Seq<u8>, right: Seq<u8>) -> bool {
    left.len() == right.len()
        && forall|i: int| #![auto] 0 <= i < left.len() ==> ascii_lower_byte(left[i]) == ascii_lower_byte(right[i])
}

#[verifier::external_body]
fn eq_ignore_ascii_case_simple(slice: &[u8], other: &[u8]) -> (ret: bool)
    requires
        slice@.len() == other@.len(),
    ensures
        ret <==> ascii_eq_ignore_case(slice@, other@),
{
    false
}

#[verifier::external_body]
fn eq_ignore_ascii_case_chunks<const N: usize>(slice: &[u8], other: &[u8]) -> (ret: bool)
    requires
        N > 0,
        slice@.len() == other@.len(),
        slice@.len() >= N as int,
    ensures
        ret <==> ascii_eq_ignore_case(slice@, other@),
{
    false
}

pub fn eq_ignore_ascii_case(slice: &[u8], other: &[u8]) -> (ret: bool)
    ensures
        ret <==> ascii_eq_ignore_case(slice@, other@),
{
    if slice.len() != other.len() {
        proof {
            assert(slice@.len() != other@.len());
            assert(!ascii_eq_ignore_case(slice@, other@));
        }
        return false;
    }

    {
        const CHUNK_SIZE: usize = 16;
        if slice.len() >= CHUNK_SIZE {
            return eq_ignore_ascii_case_chunks::<CHUNK_SIZE>(slice, other);
        }
    }

    eq_ignore_ascii_case_simple(slice, other)
}

}
