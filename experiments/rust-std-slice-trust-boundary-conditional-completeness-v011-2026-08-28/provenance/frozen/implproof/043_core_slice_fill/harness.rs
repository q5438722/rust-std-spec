#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::fill
// Source: core/src/slice/mod.rs:4166-4171 and specialize::SpecFill impls at core/src/slice/specialize.rs:4-73
// Source item sha256: e9949b7e821e39d687514cd4b39f23b69157d7ef6c845f36b8c95f1864a553d8
// Dependency manifest: proof_manifests/043_core_slice_fill/dependency_assumption_manifest.json
//
// The target now executes the Rust 1.96 default SpecFill shape: if the slice is
// non-empty, clone_from the shared value into every element except the final slot,
// then move the original value into the final slot. The retained boundary is only
// the lower per-element Clone::clone_from effect; TrivialClone and primitive
// write-bytes specializations remain equivalent source-backed lower paths.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn slice_filled_with_clone<T: core::clone::Clone>(
    old_seq: Seq<T>,
    value: T,
    dest: Seq<T>,
) -> bool {
    dest.len() == old_seq.len()
        && forall|i: int| #![auto] 0 <= i < dest.len() ==> cloned::<T>(value, dest[i])
}

pub open spec fn slice_prefix_filled_with_clone<T: core::clone::Clone>(
    old_seq: Seq<T>,
    value: T,
    dest: Seq<T>,
    count: int,
) -> bool {
    dest.len() == old_seq.len()
        && 0 <= count <= dest.len()
        && forall|i: int| 0 <= i < count ==> cloned::<T>(value, #[trigger] dest[i])
}

proof fn slice_prefix_filled_update_next<T: core::clone::Clone>(
    before: Seq<T>,
    after: Seq<T>,
    old_seq: Seq<T>,
    value: T,
    idx: int,
)
    requires
        slice_prefix_filled_with_clone(old_seq, value, before, idx),
        after.len() == before.len(),
        0 <= idx < before.len(),
        after == before.update(idx, after[idx]),
        cloned::<T>(value, after[idx]),
    ensures
        slice_prefix_filled_with_clone(old_seq, value, after, idx + 1),
{
    assert(after.len() == old_seq.len());
    assert forall|i: int| #![auto] 0 <= i < idx + 1 implies cloned::<T>(value, after[i]) by {
        if i == idx {
            assert(cloned::<T>(value, after[i]));
        } else {
            assert(0 <= i < idx);
            assert(cloned::<T>(value, before[i]));
            assert(after[i] == before[i]);
        }
    }
}

proof fn slice_complete_prefix_filled_with_clone<T: core::clone::Clone>(
    old_seq: Seq<T>,
    value: T,
    dest: Seq<T>,
)
    requires
        slice_prefix_filled_with_clone(old_seq, value, dest, dest.len() as int),
    ensures
        slice_filled_with_clone(old_seq, value, dest),
{
}

#[verifier::external_body]
pub fn rust_1_96_clone_from_value_at<T: core::clone::Clone>(
    slice: &mut [T],
    value: &T,
    idx: usize,
)
    requires
        idx < old(slice)@.len(),
    ensures
        final(slice)@.len() == old(slice)@.len(),
        final(slice)@ == old(slice)@.update(idx as int, final(slice)@[idx as int]),
        cloned::<T>(*value, final(slice)@[idx as int]),
{
    slice[idx].clone_from(value);
}

pub fn spec_fill_default_clone_loop<T: core::clone::Clone>(slice: &mut [T], value: T)
    ensures
        slice_filled_with_clone(old(slice)@, value, final(slice)@),
{
    let ghost source = slice@;
    let len = slice.len();
    if len == 0 {
        proof {
            assert(slice_prefix_filled_with_clone(source, value, slice@, 0));
            slice_complete_prefix_filled_with_clone::<T>(source, value, slice@);
        }
    } else {
        let last_index = len - 1;
        let mut idx = 0;
        proof {
            assert(slice_prefix_filled_with_clone(source, value, slice@, 0));
        }
        while idx < last_index
            invariant
                slice@.len() == source.len(),
                len as nat == source.len(),
                last_index + 1 == len,
                idx <= last_index,
                slice_prefix_filled_with_clone(source, value, slice@, idx as int),
            decreases last_index - idx
        {
            let ghost before = slice@;
            rust_1_96_clone_from_value_at(slice, &value, idx);
            proof {
                slice_prefix_filled_update_next::<T>(before, slice@, source, value, idx as int);
            }
            idx = idx + 1;
        }

        proof {
            assert(idx == last_index);
        }
        let ghost before = slice@;
        let ghost fill_value = value;
        let last = &mut slice[last_index];
        *last = value;
        proof {
            assert(slice@ == before.update(last_index as int, fill_value));
            assert(cloned::<T>(fill_value, slice@[last_index as int]));
            slice_prefix_filled_update_next::<T>(
                before,
                slice@,
                source,
                fill_value,
                last_index as int,
            );
            slice_complete_prefix_filled_with_clone::<T>(source, fill_value, slice@);
        }
    }
}

pub mod specialize {
    use vstd::prelude::*;
    use vstd::seq::*;
    use super::{slice_filled_with_clone, spec_fill_default_clone_loop};

    pub trait SpecFill<T: core::clone::Clone> {
        fn spec_fill(&mut self, value: T);
    }

    impl<T: core::clone::Clone> SpecFill<T> for [T] {
        fn spec_fill(&mut self, value: T)
            ensures
                slice_filled_with_clone(old(self)@, value, final(self)@),
        {
            spec_fill_default_clone_loop(self, value);
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
