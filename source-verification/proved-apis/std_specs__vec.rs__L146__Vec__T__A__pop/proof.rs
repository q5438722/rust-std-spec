#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::assert_seqs_equal;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

proof fn lemma_remove_last<T>(s: Seq<T>)
    requires
        s.len() > 0,
    ensures
        s.remove(s.len() - 1) == s.subrange(0, s.len() - 1),
{
    let removed = s.remove(s.len() - 1);
    let prefix = s.subrange(0, s.len() - 1);
    assert_seqs_equal!(removed, prefix, i => {
        assert(removed[i] == s[i]);
        assert(prefix[i] == s[i]);
    });
}

fn source_vec_pop<T, A: Allocator>(vec: &mut Vec<T, A>) -> (value: Option<T>)
    ensures
        old(vec)@.len() > 0 ==> value == Some(old(vec)@[old(vec)@.len() - 1])
            && final(vec)@ == old(vec)@.subrange(0, old(vec)@.len() - 1),
        old(vec)@.len() == 0 ==> value == None::<T> && final(vec)@ == old(vec)@,
{
    let len = vec.len();
    if len == 0 {
        None
    } else {
        let index = len - 1;
        let value = vec.remove(index);
        proof {
            lemma_remove_last(old(vec)@);
        }
        Some(value)
    }
}

} // verus!

fn main() {}