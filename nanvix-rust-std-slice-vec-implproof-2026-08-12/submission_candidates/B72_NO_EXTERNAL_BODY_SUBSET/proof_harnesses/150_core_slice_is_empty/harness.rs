#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::is_empty
// Source: core/src/slice/mod.rs:136-138
// Source item sha256: 8fda893dc10ecf45122b1aa88aca5cbcdb5e38a8c9abd6ecdeb3f947ac651047
// Dependency manifest: proof_manifests/150_core_slice_is_empty/dependency_assumption_manifest.json
//
// Rust 1.96 body: self.len() == 0

use vstd::prelude::*;

verus! {

pub fn is_empty<T>(slice: &[T]) -> (b: bool)
    ensures
        b <==> slice@.len() == 0,
{
    slice.len() == 0
}

}
