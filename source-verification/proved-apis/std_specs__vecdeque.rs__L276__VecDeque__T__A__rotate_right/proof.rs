#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::assert_seqs_equal;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

pub open spec fn rotated_right<T>(s: Seq<T>, n: int) -> Seq<T>
    recommends
        0 <= n <= s.len(),
{
    s.subrange(s.len() as int - n, s.len() as int)
        + s.subrange(0, s.len() as int - n)
}

pub open spec fn rotated_left<T>(s: Seq<T>, n: int) -> Seq<T>
    recommends
        0 <= n <= s.len(),
{
    s.subrange(n, s.len() as int) + s.subrange(0, n)
}

proof fn lemma_rotate_right_step<T>(s: Seq<T>, n: int)
    requires
        0 <= n < s.len(),
    ensures
        ({
            let current = rotated_right(s, n);
            seq![current[current.len() as int - 1]]
                + current.subrange(0, current.len() as int - 1)
                == rotated_right(s, n + 1)
        }),
{
    let current = rotated_right(s, n);
    let next = rotated_right(s, n + 1);
    let result = seq![current[current.len() as int - 1]]
        + current.subrange(0, current.len() as int - 1);

    assert(current.len() == s.len());
    assert_seqs_equal!(result, next, i => {
        if i == 0 {
            assert(current[current.len() as int - 1]
                == s[s.len() as int - n - 1]);
        } else if i <= n {
            assert(current[i - 1] == s[s.len() as int - n + i - 1]);
        } else {
            assert(current[i - 1] == s[i - n - 1]);
        }
    });
}

proof fn lemma_rotate_left_step<T>(s: Seq<T>, n: int)
    requires
        0 <= n < s.len(),
    ensures
        ({
            let current = rotated_left(s, n);
            current.subrange(1, current.len() as int).push(current[0])
                == rotated_left(s, n + 1)
        }),
{
    let current = rotated_left(s, n);
    let next = rotated_left(s, n + 1);
    let result = current.subrange(1, current.len() as int).push(current[0]);

    assert(current.len() == s.len());
    assert_seqs_equal!(result, next, i => {
        if i < s.len() - n - 1 {
            assert(current[i + 1] == s[n + i + 1]);
        } else if i < s.len() - 1 {
            assert(current[i + 1] == s[i - (s.len() as int - n - 1)]);
        } else {
            assert(current[0] == s[n]);
        }
    });
}

fn source_vecdeque_rotate_right<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
    n: usize,
)
    requires
        n <= old(v)@.len(),
    ensures
        final(v)@ == old(v)@.subrange(
            old(v)@.len() as int - n as int,
            old(v)@.len() as int,
        ) + old(v)@.subrange(0, old(v)@.len() as int - n as int),
{
    proof {
        axiom_spec_len(v);
    }
    if n > v.len() {
        assert(false);
        vstd::vpanic!("rotation amount should be <= len");
    }
    let k = v.len() - n;
    let ghost original = v@;

    if n <= k {
        let mut moved = 0usize;
        while moved < n
            invariant
                n <= original.len(),
                moved <= n,
                v@ == rotated_right(original, moved as int),
            decreases
                n - moved,
        {
            let value = v.pop_back();
            match value {
                Some(value) => {
                    v.push_front(value);
                },
                None => {
                    assert(false);
                },
            }
            proof {
                lemma_rotate_right_step(original, moved as int);
            }
            moved += 1;
        }
    } else {
        let mut moved = 0usize;
        while moved < k
            invariant
                k <= original.len(),
                moved <= k,
                v@ == rotated_left(original, moved as int),
            decreases
                k - moved,
        {
            let value = v.pop_front();
            match value {
                Some(value) => {
                    v.push_back(value);
                },
                None => {
                    assert(false);
                },
            }
            proof {
                lemma_rotate_left_step(original, moved as int);
            }
            moved += 1;
        }
    }
}

} // verus!

fn main() {}