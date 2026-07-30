#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use core::mem::size_of;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

fn source_vecdeque_append<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
    other: &mut VecDeque<T, A>,
)
    ensures
        final(v)@ == old(v)@ + old(other)@,
        final(other)@ == Seq::<T>::empty(),
{
    let ghost combined = v@ + other@;

    if size_of::<T>() == 0 {
        // Elementwise expansion of the ZST length transfer and reset.
        while !other.is_empty()
            invariant
                v@ + other@ == combined,
            decreases other@.len(),
        {
            let ghost v_before = v@;
            let ghost other_before = other@;
            let value = other.pop_front();
            match value {
                Some(element) => {
                    v.push_back(element);
                    proof {
                        assert(v@ + other@ =~= v_before + other_before);
                    }
                },
                None => {
                    proof {
                        assert(false);
                    }
                },
            }
        }

        proof {
            assert(other@ == Seq::<T>::empty());
            assert(v@ == combined);
        }
        return;
    }

    let count = other.len();
    v.reserve(count);

    // Elementwise expansion of the two raw slice copies and source reset.
    while !other.is_empty()
        invariant
            v@ + other@ == combined,
        decreases other@.len(),
    {
        let ghost v_before = v@;
        let ghost other_before = other@;
        let value = other.pop_front();
        match value {
            Some(element) => {
                v.push_back(element);
                proof {
                    assert(v@ + other@ =~= v_before + other_before);
                }
            },
            None => {
                proof {
                    assert(false);
                }
            },
        }
    }

    proof {
        assert(other@ == Seq::<T>::empty());
        assert(v@ == combined);
    }
}

} // verus!

fn main() {}