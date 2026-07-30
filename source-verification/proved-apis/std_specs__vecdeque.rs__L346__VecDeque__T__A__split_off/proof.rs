#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use core::clone::Clone;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

pub assume_specification<T, A: Allocator>[
    VecDeque::<T, A>::with_capacity_in
](
    capacity: usize,
    alloc: A,
) -> (result: VecDeque<T, A>)
    ensures
        result@ == Seq::<T>::empty(),
;

pub assume_specification<T, A: Allocator>[
    VecDeque::<T, A>::allocator
](
    deque: &VecDeque<T, A>,
) -> (result: &A);

fn source_vecdeque_split_off<T, A: Allocator + Clone>(
    v: &mut VecDeque<T, A>,
    at: usize,
) -> (return_value: VecDeque<T, A>)
    requires
        at <= old(v)@.len(),
    ensures
        final(v)@ == old(v)@.subrange(0, at as int),
        return_value@ == old(v)@.subrange(at as int, old(v)@.len() as int),
{
    let len = v.len();
    if at > len {
        assert(false);
        vstd::vpanic!("`at` out of bounds");
    }

    let ghost original = v@;
    proof {
        axiom_spec_len(v);
        assert(len == original.len());
    }
    let other_len = len - at;
    let mut other = VecDeque::with_capacity_in(other_len, v.allocator().clone());

    let (first_half, second_half) = v.as_slices();
    let first_len = first_half.len();
    let second_len = second_half.len();

    proof {
        assert(first_half@ + second_half@ == original);
        assert(first_len + second_len == len);
    }

    // Expand each raw copy together with the final length updates into ordered moves.
    if at < first_len {
        let amount_in_first = first_len - at;
        let mut moved_first: usize = 0;
        while moved_first < amount_in_first
            invariant
                first_len + second_len == len,
                len == original.len(),
                at < first_len,
                amount_in_first == first_len - at,
                moved_first <= amount_in_first,
                v@.len() == original.len() - moved_first,
                at + moved_first <= original.len(),
                v@ == original.subrange(0, at as int)
                    + original.subrange((at + moved_first) as int, original.len() as int),
                other@ == original.subrange(at as int, (at + moved_first) as int),
            decreases
                amount_in_first - moved_first,
        {
            assert(at < v@.len());
            let value = v.remove(at);
            match value {
                Some(element) => {
                    other.push_back(element);
                },
                None => {
                    assert(false);
                },
            }
            moved_first += 1;
        }

        let mut moved_second: usize = 0;
        while moved_second < second_len
            invariant
                first_len + second_len == len,
                len == original.len(),
                amount_in_first == first_len - at,
                moved_second <= second_len,
                v@.len() == original.len() - amount_in_first - moved_second,
                at + amount_in_first + moved_second <= original.len(),
                v@ == original.subrange(0, at as int)
                    + original.subrange(
                        (at + amount_in_first + moved_second) as int,
                        original.len() as int,
                    ),
                other@ == original.subrange(
                    at as int,
                    (at + amount_in_first + moved_second) as int,
                ),
            decreases
                second_len - moved_second,
        {
            assert(at < v@.len());
            let value = v.remove(at);
            match value {
                Some(element) => {
                    other.push_back(element);
                },
                None => {
                    assert(false);
                },
            }
            moved_second += 1;
        }
    } else {
        let offset = at - first_len;
        let amount_in_second = second_len - offset;
        let mut moved_second: usize = 0;
        while moved_second < amount_in_second
            invariant
                first_len + second_len == len,
                len == original.len(),
                first_len <= at <= len,
                offset == at - first_len,
                amount_in_second == second_len - offset,
                moved_second <= amount_in_second,
                v@.len() == original.len() - moved_second,
                at + moved_second <= original.len(),
                v@ == original.subrange(0, at as int)
                    + original.subrange(
                        (at + moved_second) as int,
                        original.len() as int,
                    ),
                other@ == original.subrange(at as int, (at + moved_second) as int),
            decreases
                amount_in_second - moved_second,
        {
            assert(at < v@.len());
            let value = v.remove(at);
            match value {
                Some(element) => {
                    other.push_back(element);
                },
                None => {
                    assert(false);
                },
            }
            moved_second += 1;
        }
    }

    proof {
        assert(v@ == original.subrange(0, at as int));
        assert(other@ == original.subrange(at as int, original.len() as int));
    }
    other
}

} // verus!

fn main() {}