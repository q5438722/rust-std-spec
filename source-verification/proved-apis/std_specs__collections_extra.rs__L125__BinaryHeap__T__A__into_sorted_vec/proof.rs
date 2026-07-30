#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::BinaryHeap;
use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::collections_extra::*;

verus! {

fn source_vec_swap<T, A: Allocator>(
    data: &mut Vec<T, A>,
    a: usize,
    b: usize,
)
    requires
        a < old(data)@.len(),
        b < old(data)@.len(),
    ensures
        final(data)@.len() == old(data)@.len(),
        final(data)@.to_multiset() == old(data)@.to_multiset(),
{
    // Safe desugaring of `ptr::swap`; splitting makes the two locations disjoint.
    if a < b {
        let ghost before = data@;
        let slice = data.as_mut_slice();
        let (left, right) = slice.split_at_mut(b);
        core::mem::swap(&mut left[a], &mut right[0]);
        proof {
            assert(data@ == before.update(a as int, before[b as int]).update(
                b as int,
                before[a as int],
            ));
        }
    } else if b < a {
        let ghost before = data@;
        let slice = data.as_mut_slice();
        let (left, right) = slice.split_at_mut(a);
        core::mem::swap(&mut left[b], &mut right[0]);
        proof {
            assert(data@ == before.update(b as int, before[a as int]).update(
                a as int,
                before[b as int],
            ));
        }
    }
    proof {
        broadcast use vstd::multiset::group_multiset_axioms;
        broadcast use vstd::seq_lib::group_to_multiset_ensures;
        assert(data@.to_multiset() =~= old(data)@.to_multiset());
    }
}

#[verifier::exec_allows_no_decreases_clause]
fn source_sift_down_range<T: Ord, A: Allocator>(
    data: &mut Vec<T, A>,
    pos: usize,
    end: usize,
) -> (result: usize)
    requires
        pos < end,
        end <= old(data)@.len(),
    ensures
        final(data)@.len() == old(data)@.len(),
        final(data)@.to_multiset() == old(data)@.to_multiset(),
{
    let mut hole_pos = pos;
    let mut child = hole_pos.wrapping_mul(2).wrapping_add(1);

    // Swapping the sifted element with each selected child is the fully
    // initialized equivalent of the source's `Hole::move_to` operations.
    while end >= 2 && child <= end - 2
        invariant
            end <= data@.len(),
            data@.len() == old(data)@.len(),
            data@.to_multiset() == old(data)@.to_multiset(),
            hole_pos < end,
    {
        if data[child] <= data[child + 1] {
            child += 1;
        }

        if data[hole_pos] >= data[child] {
            return hole_pos;
        }

        source_vec_swap(data, hole_pos, child);
        hole_pos = child;
        child = hole_pos.wrapping_mul(2).wrapping_add(1);
    }

    if child == end - 1 && data[hole_pos] < data[child] {
        source_vec_swap(data, hole_pos, child);
        hole_pos = child;
    }

    hole_pos
}

fn source_binary_heap_into_sorted_vec<T: Ord, A: Allocator>(
    heap: BinaryHeap<T, A>,
) -> (result: Vec<T, A>)
    ensures
        result@.to_multiset() == heap@,
{
    let mut end = heap.len();
    // `into_vec` moves out the private `self.data`; moving it before the loop
    // exposes the same allocation on which the source performs heap sort.
    let mut data = heap.into_vec();
    proof {
        broadcast use vstd::seq_lib::group_to_multiset_ensures;
        assert(end as nat == data@.len());
    }
    while end > 1
        invariant
            end <= data@.len(),
            data@.to_multiset() == heap@,
        decreases end,
    {
        end -= 1;
        source_vec_swap(&mut data, 0, end);
        source_sift_down_range(&mut data, 0, end);
    }
    data
}

} // verus!

fn main() {}