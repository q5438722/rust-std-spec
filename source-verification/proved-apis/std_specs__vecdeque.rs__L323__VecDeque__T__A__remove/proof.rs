#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::assert_seqs_equal;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

pub open spec fn shifted_right<T>(s: Seq<T>, index: int, cursor: int) -> Seq<T>
    recommends
        0 <= index <= cursor < s.len(),
{
    Seq::new(
        s.len(),
        |j: int|
            if j < index {
                s[j]
            } else if j < cursor {
                s[j + 1]
            } else if j == cursor {
                s[index]
            } else {
                s[j]
            },
    )
}

pub open spec fn shifted_left<T>(s: Seq<T>, index: int, cursor: int) -> Seq<T>
    recommends
        0 <= cursor <= index < s.len(),
{
    Seq::new(
        s.len(),
        |j: int|
            if j < cursor {
                s[j]
            } else if j == cursor {
                s[index]
            } else if j <= index {
                s[j - 1]
            } else {
                s[j]
            },
    )
}

proof fn lemma_shifted_right_initial<T>(s: Seq<T>, index: int)
    requires
        0 <= index < s.len(),
    ensures
        shifted_right(s, index, index) == s,
{
    assert_seqs_equal!(shifted_right(s, index, index), s, j => {});
}

proof fn lemma_shifted_right_step<T>(s: Seq<T>, index: int, cursor: int)
    requires
        0 <= index <= cursor,
        cursor + 1 < s.len(),
    ensures
        shifted_right(s, index, cursor).update(
            cursor,
            shifted_right(s, index, cursor)[cursor + 1],
        ).update(
            cursor + 1,
            shifted_right(s, index, cursor)[cursor],
        ) == shifted_right(s, index, cursor + 1),
{
    let before = shifted_right(s, index, cursor);
    let after = before.update(cursor, before[cursor + 1]).update(
        cursor + 1,
        before[cursor],
    );
    assert(before[cursor] == s[index]);
    assert(before[cursor + 1] == s[cursor + 1]);
    assert_seqs_equal!(after, shifted_right(s, index, cursor + 1), j => {
        if j == cursor {
            assert(after[j] == s[cursor + 1]);
        } else if j == cursor + 1 {
            assert(after[j] == s[index]);
        }
    });
}

proof fn lemma_shifted_right_finish<T>(s: Seq<T>, index: int)
    requires
        0 <= index < s.len(),
    ensures
        shifted_right(s, index, s.len() as int - 1)[s.len() as int - 1] == s[index],
        shifted_right(s, index, s.len() as int - 1).subrange(
            0,
            s.len() as int - 1,
        ) == s.remove(index),
{
    let shifted = shifted_right(s, index, s.len() as int - 1);
    assert(shifted[s.len() as int - 1] == s[index]);
    assert_seqs_equal!(
        shifted.subrange(0, s.len() as int - 1),
        s.remove(index),
        j => {
            if j < index {
                assert(shifted[j] == s[j]);
            } else {
                assert(shifted[j] == s[j + 1]);
            }
        }
    );
}

proof fn lemma_shifted_left_initial<T>(s: Seq<T>, index: int)
    requires
        0 <= index < s.len(),
    ensures
        shifted_left(s, index, index) == s,
{
    assert_seqs_equal!(shifted_left(s, index, index), s, j => {});
}

proof fn lemma_shifted_left_step<T>(s: Seq<T>, index: int, cursor: int)
    requires
        0 < cursor <= index,
        index < s.len(),
    ensures
        shifted_left(s, index, cursor).update(
            cursor,
            shifted_left(s, index, cursor)[cursor - 1],
        ).update(
            cursor - 1,
            shifted_left(s, index, cursor)[cursor],
        ) == shifted_left(s, index, cursor - 1),
{
    let before = shifted_left(s, index, cursor);
    let after = before.update(cursor, before[cursor - 1]).update(
        cursor - 1,
        before[cursor],
    );
    assert(before[cursor] == s[index]);
    assert(before[cursor - 1] == s[cursor - 1]);
    assert_seqs_equal!(after, shifted_left(s, index, cursor - 1), j => {
        if j == cursor - 1 {
            assert(after[j] == s[index]);
        } else if j == cursor {
            assert(after[j] == s[cursor - 1]);
        }
    });
}

proof fn lemma_shifted_left_finish<T>(s: Seq<T>, index: int)
    requires
        0 <= index < s.len(),
    ensures
        shifted_left(s, index, 0)[0] == s[index],
        shifted_left(s, index, 0).subrange(1, s.len() as int) == s.remove(index),
{
    let shifted = shifted_left(s, index, 0);
    assert(shifted[0] == s[index]);
    assert_seqs_equal!(
        shifted.subrange(1, s.len() as int),
        s.remove(index),
        j => {
            if j < index {
                assert(shifted[j + 1] == s[j]);
            } else {
                assert(shifted[j + 1] == s[j + 1]);
            }
        }
    );
}

fn source_vecdeque_remove<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
    index: usize,
) -> (element: Option<T>)
    ensures
        match element {
            Some(x) => {
                &&& index < old(v)@.len()
                &&& x == old(v)@[index as int]
                &&& final(v)@ == old(v)@.remove(index as int)
            },
            None => {
                &&& old(v)@.len() <= index
                &&& final(v)@ == old(v)@
            },
        },
{
    proof {
        axiom_spec_len(v);
    }
    let len = v.len();
    if len <= index {
        return None;
    }

    let ghost original = v@;
    let k = len - index - 1;

    // Safe elementwise desugaring of buffer_read plus the selected wrap_copy.
    let elem = if k < index {
        let mut cursor = index;
        proof {
            lemma_shifted_right_initial(original, index as int);
        }
        while cursor + 1 < len
            invariant
                len == original.len(),
                index < len,
                index <= cursor < len,
                v@ == shifted_right(original, index as int, cursor as int),
            decreases
                len - cursor - 1,
        {
            let ghost before = v@;
            v.swap(cursor, cursor + 1);
            proof {
                lemma_shifted_right_step(original, index as int, cursor as int);
                assert(v@ == before.update(cursor as int, before[(cursor + 1) as int]).update(
                    (cursor + 1) as int,
                    before[cursor as int],
                ));
            }
            cursor += 1;
        }
        proof {
            lemma_shifted_right_finish(original, index as int);
        }
        v.pop_back()
    } else {
        let mut cursor = index;
        proof {
            lemma_shifted_left_initial(original, index as int);
        }
        while cursor > 0
            invariant
                len == original.len(),
                index < len,
                cursor <= index,
                v@ == shifted_left(original, index as int, cursor as int),
            decreases
                cursor,
        {
            let ghost before = v@;
            v.swap(cursor, cursor - 1);
            proof {
                lemma_shifted_left_step(original, index as int, cursor as int);
                assert(v@ == before.update(cursor as int, before[(cursor - 1) as int]).update(
                    (cursor - 1) as int,
                    before[cursor as int],
                ));
            }
            cursor -= 1;
        }
        proof {
            lemma_shifted_left_finish(original, index as int);
        }
        v.pop_front()
    };

    match elem {
        Some(value) => Some(value),
        None => {
            assert(false);
            None
        },
    }
}

} // verus!

fn main() {}