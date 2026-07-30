#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

fn source_vec_swap_remove<T, A: Allocator>(
    vec: &mut Vec<T, A>,
    index: usize,
) -> (element: T)
    requires
        index < old(vec).len(),
    ensures
        element == old(vec)[index as int],
        final(vec)@ == old(vec)@.update(index as int, old(vec)@.last()).drop_last(),
{
    let len = vec.len();
    if index >= len {
        assert(false);
        vstd::vpanic!(
            "swap_remove index (is {}) should be < len (is {})",
            index,
            len
        );
    }

    // Safe desugaring of the source's read/copy: put the removed value last.
    if index < len - 1 {
        let ghost before = vec@;
        let slice = vec.as_mut_slice();
        let (prefix, last) = slice.split_at_mut(len - 1);
        core::mem::swap(&mut prefix[index], &mut last[0]);
        proof {
            assert(vec@ == before.update(index as int, before[(len - 1) as int]).update(
                (len - 1) as int,
                before[index as int],
            ));
        }
    }

    let ghost before_remove = vec@;
    let element = vec.remove(len - 1);
    proof {
        assert(element == before_remove[(len - 1) as int]);
        assert(vec@ == before_remove.remove((len - 1) as int));
    }
    element
}

} // verus!

fn main() {}