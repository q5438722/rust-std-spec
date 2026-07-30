#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

fn source_vec_append<T, A: Allocator>(
    vec: &mut Vec<T, A>,
    other: &mut Vec<T, A>,
)
    ensures
        final(vec)@ == old(vec)@ + old(other)@,
        final(other)@ == Seq::<T>::empty(),
{
    let ghost combined = vec@ + other@;
    let count = other.len();
    vec.reserve(count);
    let _len = vec.len();

    if count > 0 {
        // Elementwise move expansion of `copy_nonoverlapping` followed by `set_len(0)`.
        while !other.is_empty()
            invariant
                vec@ + other@ == combined,
            decreases other@.len(),
        {
            let ghost vec_before = vec@;
            let ghost other_before = other@;
            let value = other.remove(0);
            vec.push(value);

            proof {
                assert(vec@ + other@ =~= vec_before + other_before);
            }
        }
    }

    proof {
        assert(other@.len() == 0);
        assert(other@ == Seq::<T>::empty());
        assert(vec@ == combined);
    }
}

} // verus!

fn main() {}