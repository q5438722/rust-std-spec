#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

fn source_vec_truncate<T, A: Allocator>(vec: &mut Vec<T, A>, len: usize)
    ensures
        len <= old(vec).len() ==> final(vec)@ == old(vec)@.subrange(0, len as int),
        len > old(vec).len() ==> final(vec)@ == old(vec)@,
{
    if len > vec.len() {
        return;
    }

    let ghost original = vec@;
    let remaining_len = vec.len() - len;
    let mut dropped: usize = 0;

    // Elementwise expansion of shrinking `self.len` and dropping the tail slice.
    while dropped < remaining_len
        invariant
            len <= original.len(),
            remaining_len == original.len() - len,
            dropped <= remaining_len,
            vec@ == original.subrange(0, len as int)
                + original.subrange((len + dropped) as int, original.len() as int),
        decreases
            remaining_len - dropped,
    {
        let _ = vec.remove(len);
        dropped += 1;
    }

    assert(len + dropped == original.len());
    assert(original.subrange(original.len() as int, original.len() as int)
        == Seq::<T>::empty());
    assert(vec@ == original.subrange(0, len as int));
}

} // verus!

fn main() {}