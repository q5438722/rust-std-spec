#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::fill
// Source: core/src/slice/mod.rs:4166-4171 and specialize::SpecFill impls at core/src/slice/specialize.rs:4-73
// Source item sha256: e9949b7e821e39d687514cd4b39f23b69157d7ef6c845f36b8c95f1864a553d8
// Dependency manifest: proof_manifests/043_core_slice_fill/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn slice_filled_with_clone<T: core::clone::Clone>(
    old_seq: Seq<T>,
    value: T,
    dest: Seq<T>,
) -> bool {
    dest.len() == old_seq.len()
        && forall|i: int| 0 <= i < dest.len() ==> cloned::<T>(value, dest[i])
}

pub mod specialize {
    use vstd::prelude::*;
    use vstd::seq::*;
    use super::slice_filled_with_clone;

    pub trait SpecFill<T: core::clone::Clone> {
        fn spec_fill(&mut self, value: T);
    }

    impl<T: core::clone::Clone> SpecFill<T> for [T] {
        #[verifier::external_body]
        fn spec_fill(&mut self, value: T)
            ensures
                slice_filled_with_clone(old(self)@, value, final(self)@),
        {
        }
    }
}

pub fn fill<T: core::clone::Clone>(slice: &mut [T], value: T)
    ensures
        slice_filled_with_clone(old(slice)@, value, final(slice)@),
{
    specialize::SpecFill::spec_fill(slice, value);
}

}
