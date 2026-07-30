#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use core::clone::Clone;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

pub assume_specification<T, A: Allocator>[
    Vec::<T, A>::allocator
](
    vec: &Vec<T, A>,
) -> (result: &A);

fn source_vec_split_off<T, A: Allocator + Clone>(
    vec: &mut Vec<T, A>,
    at: usize,
) -> (return_value: Vec<T, A>)
    requires
        at <= old(vec)@.len(),
    ensures
        final(vec)@ == old(vec)@.subrange(0, at as int),
        return_value@ == old(vec)@.subrange(at as int, old(vec)@.len() as int),
{
    if at > vec.len() {
        assert(false);
        vstd::vpanic!("`at` split index should be <= len");
    }

    let ghost original = vec@;
    let other_len = vec.len() - at;
    let mut other = Vec::with_capacity_in(other_len, vec.allocator().clone());

    // Elementwise expansion of the `set_len` and `copy_nonoverlapping` block.
    let mut moved: usize = 0;
    while moved < other_len
        invariant
            at <= original.len(),
            other_len == original.len() - at,
            moved <= other_len,
            vec@ == original.subrange(0, at as int)
                + original.subrange((at + moved) as int, original.len() as int),
            other@ == original.subrange(at as int, (at + moved) as int),
        decreases
            other_len - moved,
    {
        let value = vec.remove(at);
        other.push(value);
        moved += 1;
    }

    assert(at + moved == original.len());
    assert(original.subrange(original.len() as int, original.len() as int)
        == Seq::<T>::empty());
    assert(vec@ == original.subrange(0, at as int));
    assert(other@ == original.subrange(at as int, original.len() as int));
    other
}

} // verus!

fn main() {}