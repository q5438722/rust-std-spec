#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::fill_with
// Source: core/src/slice/mod.rs:4190-4197
// Source item sha256: a8850a1c2400e9f212f3ebdadf7f8ed4c286c67e9a31275914960d3c78479e48
// Dependency manifest: proof_manifests/044_core_slice_fill_with/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn zero_arg_fnmut_outputs<F, T>(f: F, len: nat) -> Seq<T>;

pub broadcast axiom fn axiom_zero_arg_fnmut_outputs_len<F, T>(f: F, len: nat)
    ensures
        #[trigger] zero_arg_fnmut_outputs::<F, T>(f, len).len() == len,
;

#[verifier::external_body]
fn zero_arg_fnmut_call_at<T, F: FnMut() -> T>(
    f: &mut F,
    Ghost(outputs): Ghost<Seq<T>>,
    Ghost(index): Ghost<int>,
) -> (value: T)
    requires
        0 <= index < outputs.len(),
    ensures
        value == outputs[index],
{
    f()
}

pub fn fill_with<T, F: FnMut() -> T>(slice: &mut [T], f: F)
    ensures
        final(slice)@ == zero_arg_fnmut_outputs::<F, T>(f, old(slice)@.len()),
        zero_arg_fnmut_outputs::<F, T>(f, old(slice)@.len()).len() == old(slice)@.len(),
{
    let ghost outputs = zero_arg_fnmut_outputs::<F, T>(f, old(slice)@.len());
    let ghost source = slice@;
    proof {
        axiom_zero_arg_fnmut_outputs_len::<F, T>(f, old(slice)@.len());
    }
    let mut f = f;
    let mut i = 0;
    while i < slice.len()
        invariant
            0 <= i <= slice@.len(),
            slice@.len() == source.len(),
            outputs.len() == source.len(),
            forall|j: int| #![auto] 0 <= j < i ==> slice@[j] == outputs[j],
            forall|j: int| #![auto] i <= j < slice@.len() ==> slice@[j] == source[j],
        decreases slice.len() - i
    {
        let value = zero_arg_fnmut_call_at(&mut f, Ghost(outputs), Ghost(i as int));
        let el = &mut slice[i];
        *el = value;
        i += 1;
    }
}

}
