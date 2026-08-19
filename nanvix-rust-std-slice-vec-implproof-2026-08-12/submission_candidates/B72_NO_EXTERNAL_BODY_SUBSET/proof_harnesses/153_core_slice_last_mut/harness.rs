#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::last_mut
// Source: core/src/slice/mod.rs:304-306
// Source item sha256: 9cc6fb48c09b16ab3bd758b27666b2f815f072148ec53e86e3e8a17531d23ad6
// Dependency manifest: proof_manifests/153_core_slice_last_mut/dependency_assumption_manifest.json
//
// Rust 1.96 body: if let [.., last] = self { Some(last) } else { None }

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub fn last_mut<'a, T>(slice: &'a mut [T]) -> (ret: Option<&'a mut T>)
    ensures
        old(slice)@.len() == 0 ==> ret.is_none() && final(slice)@ == old(slice)@,
        old(slice)@.len() != 0 ==> ret.is_some()
            && *ret.unwrap() == old(slice)@[(old(slice)@.len() - 1) as int]
            && final(slice)@ == old(slice)@.update(
                (old(slice)@.len() - 1) as int,
                *final(ret.unwrap()),
            ),
{
    if slice.len() != 0 {
        let ghost source = slice@;
        let split = slice.len() - 1;
        let (init, tail) = slice.split_at_mut(split);
        proof {
            assert(split as int == source.len() - 1);
            source.lemma_split_at(split as int);
            assert(init@ =~= source.subrange(0, split as int));
            assert(tail@ =~= source.subrange(split as int, source.len() as int));
            assert(tail@.len() == 1);
            assert(tail@[0] == source[(source.len() - 1) as int]);
        }
        let last = &mut tail[0];
        proof {
            assert(source.subrange(0, (source.len() - 1) as int) + seq![*final(last)]
                =~= source.update((source.len() - 1) as int, *final(last)));
        }
        Some(last)
    } else {
        None
    }
}

}
