#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::last
// Source: core/src/slice/mod.rs:281-283
// Source item sha256: f1246fd95d78a6272bd35954b283765660c90b041fd31d41891264a19a3e4bdd
// Dependency manifest: proof_manifests/152_core_slice_last/dependency_assumption_manifest.json
//
// Rust 1.96 body: if let [.., last] = self { Some(last) } else { None }

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub fn last<'a, T>(slice: &'a [T]) -> (ret: Option<&'a T>)
    ensures
        slice@.len() == 0 ==> ret.is_none(),
        slice@.len() != 0 ==> ret.is_some() && *ret.unwrap() == slice@.last(),
{
    if slice.len() != 0 {
        let split = slice.len() - 1;
        let (_init, tail) = slice.split_at(split);
        proof {
            assert(split as int == slice@.len() - 1);
            slice@.lemma_split_at(split as int);
            assert(tail@ =~= slice@.subrange(split as int, slice@.len() as int));
            assert(tail@.len() == 1);
            assert(tail@[0] == slice@[(slice@.len() - 1) as int]);
            assert(slice@.last() == slice@[(slice@.len() - 1) as int]);
        }
        let last = &tail[0];
        proof {
            assert(*last == tail@[0]);
        }
        Some(last)
    } else {
        None
    }
}

}
