#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::from_mut
// Source: core/src/slice/raw.rs:211-213
// Source item sha256: 9dccff9babfff3c297268487fbf17b0a6ca139a9d1de3ef5c1163f9995eb7235
// Dependency manifest: proof_manifests/047_core_slice_from_mut/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub mod array {
    use vstd::prelude::*;
    use vstd::seq::*;

    #[verifier::external_body]
    pub fn from_mut<'a, T>(s: &'a mut T) -> (ret: &'a mut [T])
        ensures
            ret@ == seq![*old(s)],
            final(ret)@ == seq![*final(s)],
    {
        &mut []
    }
}

pub fn from_mut<'a, T>(s: &'a mut T) -> (ret: &'a mut [T])
    ensures
        ret@ == seq![*old(s)],
        final(ret)@ == seq![*final(s)],
{
    array::from_mut(s)
}

}
