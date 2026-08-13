#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::first
// Source: core/src/slice/mod.rs:155-157
// Source item sha256: 7761aa6f658ec92f2d144741f2022cf409365957b0e1487d24bbdf15d2b9151d
// Dependency manifest: proof_manifests/147_core_slice_first/dependency_assumption_manifest.json
//
// Rust 1.96 body: if let [first, ..] = self { Some(first) } else { None }

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub fn first<'a, T>(slice: &'a [T]) -> (ret: Option<&'a T>)
    ensures
        slice@.len() == 0 ==> ret.is_none(),
        slice@.len() != 0 ==> ret.is_some() && *ret.unwrap() == slice@[0],
{
    if slice.len() != 0 {
        let (head, _tail) = slice.split_at(1);
        let first = &head[0];
        proof {
            slice@.lemma_split_at(1);
            assert(head@ =~= slice@.subrange(0, 1));
            assert(*first == head@[0]);
            assert(head@[0] == slice@[0]);
        }
        Some(first)
    } else {
        None
    }
}

}
