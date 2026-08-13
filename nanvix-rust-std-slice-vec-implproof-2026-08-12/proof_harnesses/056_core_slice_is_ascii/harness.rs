#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::is_ascii
// Source: core/src/slice/ascii.rs:18-20 and active x86_64+sse2 private helper at lines 541-607
// Source item sha256: 005d9271af4c5322c1e5b50e48a1bd6a1d364367072e3fe1870a6aa0f0a1b492
// Dependency manifest: proof_manifests/056_core_slice_is_ascii/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn ascii_is_byte(byte: u8) -> bool {
    (byte as int) <= 0x7f
}

pub open spec fn ascii_all(seq: Seq<u8>) -> bool {
    forall|i: int| #![auto] 0 <= i < seq.len() ==> ascii_is_byte(seq[i])
}

#[verifier::external_body]
fn private_is_ascii(bytes: &[u8]) -> (ret: bool)
    ensures
        ret <==> ascii_all(bytes@),
{
    false
}

pub fn is_ascii(slice: &[u8]) -> (ret: bool)
    ensures
        ret <==> ascii_all(slice@),
{
    private_is_ascii(slice)
}

}
