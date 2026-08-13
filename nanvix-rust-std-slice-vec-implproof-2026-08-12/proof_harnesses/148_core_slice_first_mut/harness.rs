#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::first_mut
// Source: core/src/slice/mod.rs:178-180
// Source item sha256: acca42d75b023fc555162973f3a3b5beaa11eb77d07e21b6405b09e18203d00b
// Dependency manifest: proof_manifests/148_core_slice_first_mut/dependency_assumption_manifest.json
//
// Rust 1.96 body: if let [first, ..] = self { Some(first) } else { None }

use vstd::prelude::*;
use vstd::seq::*;

verus! {

proof fn lemma_update_first<T>(source: Seq<T>, value: T)
    requires
        source.len() > 0,
    ensures
        seq![value] + source.subrange(1, source.len() as int) =~= source.update(0, value),
{
    assert(seq![value] + source.subrange(1, source.len() as int) =~= source.update(0, value));
}

pub fn first_mut<'a, T>(slice: &'a mut [T]) -> (ret: Option<&'a mut T>)
    ensures
        old(slice)@.len() == 0 ==> ret.is_none() && final(slice)@ == old(slice)@,
        old(slice)@.len() != 0 ==> ret.is_some()
            && *ret.unwrap() == old(slice)@[0]
            && final(slice)@ == old(slice)@.update(0, *final(ret.unwrap())),
{
    if slice.len() != 0 {
        let ghost source = slice@;
        let (head, tail) = slice.split_at_mut(1);
        proof {
            source.lemma_split_at(1);
            assert(head@ =~= source.subrange(0, 1));
            assert(tail@ =~= source.subrange(1, source.len() as int));
            assert(head@[0] == source[0]);
        }
        let first = &mut head[0];
        proof {
            lemma_update_first(source, *final(first));
        }
        Some(first)
    } else {
        None
    }
}

}
