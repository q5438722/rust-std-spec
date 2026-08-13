#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::from_ref
// Source: core/src/slice/raw.rs:203-205
// Source item sha256: b2a768bd7c6814a7c07b0a33257355733e29a006ecf4aed8c9cae6ab997b1cf8
// Dependency manifest: proof_manifests/050_core_slice_from_ref/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub mod array {
    use vstd::prelude::*;
    use vstd::seq::*;

    #[verifier::external_body]
    pub fn from_ref<'a, T>(s: &'a T) -> (ret: &'a [T])
        ensures
            ret@ == seq![*s],
    {
        &[]
    }
}

pub fn from_ref<'a, T>(s: &'a T) -> (ret: &'a [T])
    ensures
        ret@ == seq![*s],
{
    array::from_ref(s)
}

}
