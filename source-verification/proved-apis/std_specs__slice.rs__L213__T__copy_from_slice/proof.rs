#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::slice::*;

verus! {

fn source_slice_copy_from_slice<T: Copy>(dst: &mut [T], src: &[T])
    requires
        old(dst)@.len() == src@.len(),
    ensures
        final(dst)@ == src@,
{
    if dst.len() != src.len() {
        assert(false);
        vstd::vpanic!(
            "copy_from_slice: source slice length does not match destination slice length"
        );
    }

    // Elementwise expansion of `copy_nonoverlapping`; the two borrows are disjoint.
    let mut idx: usize = 0;
    while idx < dst.len()
        invariant
            idx <= dst@.len(),
            dst@.len() == src@.len(),
            forall|j: int| 0 <= j < idx ==> dst@[j] == src@[j],
        decreases
            dst@.len() - idx,
    {
        let ghost prev_dst = dst@;
        let value = src[idx];
        dst[idx] = value;
        assert forall|j: int| 0 <= j < idx + 1 implies dst@[j] == src@[j] by {
            if j < idx {
                assert(prev_dst[j] == src@[j]);
                assert(dst@[j] == prev_dst[j]);
            } else {
                assert(j == idx);
            }
        }
        idx += 1;
    }

    assert(dst@ =~= src@);
}

} // verus!

fn main() {}