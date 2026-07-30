#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::assert_seqs_equal;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

proof fn lemma_remove_last<T>(s: Seq<T>)
    requires
        s.len() > 0,
    ensures
        s.remove(s.len() - 1) == s.subrange(0, s.len() as int - 1),
{
    let removed = s.remove(s.len() - 1);
    let prefix = s.subrange(0, s.len() as int - 1);
    assert_seqs_equal!(removed, prefix, i => {
        assert(removed[i] == s[i]);
        assert(prefix[i] == s[i]);
    });
}

fn source_vecdeque_pop_back<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
) -> (value: Option<T>)
    ensures
        match value {
            Some(x) => {
                &&& old(v)@.len() > 0
                &&& x == old(v)@[old(v)@.len() - 1]
                &&& final(v)@ == old(v)@.subrange(0, old(v)@.len() as int - 1)
            },
            None => {
                &&& old(v)@.len() == 0
                &&& final(v)@ == old(v)@
            },
        },
{
    if v.is_empty() {
        None
    } else {
        let len = v.len();
        let value = v.remove(len - 1);
        proof {
            axiom_spec_len(old(v));
            lemma_remove_last(old(v)@);
        }
        value
    }
}

} // verus!

fn main() {}