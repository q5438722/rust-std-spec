#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::assert_seqs_equal;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

proof fn lemma_remove_first<T>(s: Seq<T>)
    requires
        s.len() > 0,
    ensures
        s.remove(0) == s.subrange(1, s.len() as int),
{
    let removed = s.remove(0);
    let tail = s.subrange(1, s.len() as int);
    assert_seqs_equal!(removed, tail, i => {
        assert(removed[i] == s[i + 1]);
        assert(tail[i] == s[i + 1]);
    });
}

fn source_vecdeque_pop_front<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
) -> (value: Option<T>)
    ensures
        match value {
            Some(x) => {
                &&& old(v)@.len() > 0
                &&& x == old(v)@[0]
                &&& final(v)@ == old(v)@.subrange(1, old(v)@.len() as int)
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
        let value = v.remove(0);
        proof {
            lemma_remove_first(old(v)@);
        }
        value
    }
}

} // verus!

fn main() {}