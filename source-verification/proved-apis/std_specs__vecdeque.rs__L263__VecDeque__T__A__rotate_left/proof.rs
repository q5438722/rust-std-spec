#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::assert_seqs_equal;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

proof fn lemma_rotate_left_one<T>(s: Seq<T>, i: int)
    requires
        0 <= i < s.len(),
    ensures
        (s.subrange(i, s.len() as int) + s.subrange(0, i)).subrange(
            1,
            s.len() as int,
        ).push((s.subrange(i, s.len() as int) + s.subrange(0, i))[0])
            == s.subrange(i + 1, s.len() as int) + s.subrange(0, i + 1),
{
    let before = s.subrange(i, s.len() as int) + s.subrange(0, i);
    let after = before.subrange(1, s.len() as int).push(before[0]);
    let expected = s.subrange(i + 1, s.len() as int) + s.subrange(0, i + 1);
    assert_seqs_equal!(after, expected, j => {
        if j < s.len() - i - 1 {
            assert(after[j] == before[j + 1]);
            assert(before[j + 1] == s[i + j + 1]);
            assert(expected[j] == s[i + j + 1]);
        } else if j < s.len() - 1 {
            assert(after[j] == before[j + 1]);
            assert(before[j + 1] == s[j - (s.len() - i - 1)]);
            assert(expected[j] == s[j - (s.len() - i - 1)]);
        } else {
            assert(j == s.len() - 1);
            assert(after[j] == before[0]);
            assert(before[0] == s[i]);
            assert(expected[j] == s[i]);
        }
    });
}

proof fn lemma_rotate_right_one<T>(s: Seq<T>, i: int)
    requires
        0 <= i < s.len(),
    ensures
        seq![
            (s.subrange(s.len() as int - i, s.len() as int)
                + s.subrange(0, s.len() as int - i))[s.len() as int - 1]
        ] + (s.subrange(s.len() as int - i, s.len() as int)
            + s.subrange(0, s.len() as int - i)).subrange(
            0,
            s.len() as int - 1,
        )
            == s.subrange(s.len() as int - i - 1, s.len() as int)
                + s.subrange(0, s.len() as int - i - 1),
{
    let before = s.subrange(s.len() as int - i, s.len() as int)
        + s.subrange(0, s.len() as int - i);
    let after = seq![before[s.len() as int - 1]]
        + before.subrange(0, s.len() as int - 1);
    let expected = s.subrange(s.len() as int - i - 1, s.len() as int)
        + s.subrange(0, s.len() as int - i - 1);
    assert_seqs_equal!(after, expected, j => {
        if j == 0 {
            assert(before[s.len() as int - 1] == s[s.len() as int - i - 1]);
            assert(after[j] == s[s.len() as int - i - 1]);
            assert(expected[j] == s[s.len() as int - i - 1]);
        } else if j <= i {
            assert(after[j] == before[j - 1]);
            assert(before[j - 1] == s[s.len() as int - i + j - 1]);
            assert(expected[j] == s[s.len() as int - i + j - 1]);
        } else {
            assert(after[j] == before[j - 1]);
            assert(before[j - 1] == s[j - i - 1]);
            assert(expected[j] == s[j - i - 1]);
        }
    });
}

fn source_rotate_left_inner<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
    mid: usize,
)
    requires
        mid <= old(v)@.len(),
    ensures
        final(v)@ == old(v)@.subrange(mid as int, old(v)@.len() as int)
            + old(v)@.subrange(0, mid as int),
{
    let ghost original = v@;
    let mut moved: usize = 0;
    while moved < mid
        invariant
            mid <= original.len(),
            moved <= mid,
            v@ == original.subrange(moved as int, original.len() as int)
                + original.subrange(0, moved as int),
        decreases
            mid - moved,
    {
        let front = v.pop_front();
        match front {
            Some(value) => {
                v.push_back(value);
                proof {
                    lemma_rotate_left_one(original, moved as int);
                }
            },
            None => {
                assert(false);
                vstd::vpanic!("nonempty VecDeque became empty during rotate_left")
            },
        }
        moved += 1;
    }
}

fn source_rotate_right_inner<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
    k: usize,
)
    requires
        k <= old(v)@.len(),
    ensures
        final(v)@ == old(v)@.subrange(
            old(v)@.len() as int - k as int,
            old(v)@.len() as int,
        ) + old(v)@.subrange(0, old(v)@.len() as int - k as int),
{
    let ghost original = v@;
    let mut moved: usize = 0;
    proof {
        assert_seqs_equal!(
            original,
            original.subrange(original.len() as int, original.len() as int)
                + original.subrange(0, original.len() as int)
        );
    }
    while moved < k
        invariant
            k <= original.len(),
            moved <= k,
            v@ == original.subrange(
                original.len() as int - moved as int,
                original.len() as int,
            ) + original.subrange(
                0,
                original.len() as int - moved as int,
            ),
        decreases
            k - moved,
    {
        let back = v.pop_back();
        match back {
            Some(value) => {
                v.push_front(value);
                proof {
                    lemma_rotate_right_one(original, moved as int);
                }
            },
            None => {
                assert(false);
                vstd::vpanic!("nonempty VecDeque became empty during rotate_right")
            },
        }
        moved += 1;
    }
}

fn source_vecdeque_rotate_left<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
    n: usize,
)
    requires
        n <= old(v)@.len(),
    ensures
        final(v)@ == old(v)@.subrange(n as int, old(v)@.len() as int)
            + old(v)@.subrange(0, n as int),
{
    if n > v.len() {
        assert(false);
        vstd::vpanic!("rotation amount exceeds VecDeque length");
    }
    let k = v.len() - n;
    if n <= k {
        source_rotate_left_inner(v, n)
    } else {
        source_rotate_right_inner(v, k)
    }
}

} // verus!

fn main() {}