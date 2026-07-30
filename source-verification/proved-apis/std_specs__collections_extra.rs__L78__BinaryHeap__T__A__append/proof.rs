#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::BinaryHeap;
use alloc::vec::Vec;
use core::alloc::Allocator;
use core::mem::swap;
use vstd::multiset::Multiset;
use vstd::prelude::*;
use vstd::std_specs::collections_extra::*;

unsafe fn binary_heap_data_mut_rust_1_96<'a, T, A: Allocator>(
    heap: &'a mut BinaryHeap<T, A>,
) -> &'a mut Vec<T, A> {
    unsafe { &mut *(heap as *mut BinaryHeap<T, A> as *mut Vec<T, A>) }
}

verus! {

pub assume_specification<T, A: Allocator>[binary_heap_data_mut_rust_1_96](
    heap: &mut BinaryHeap<T, A>,
) -> (data: &mut Vec<T, A>)
    ensures
        data@.to_multiset() == old(heap)@,
        final(data)@.to_multiset() == final(heap)@,
;

pub assume_specification[usize::leading_zeros](value: usize) -> (result: u32)
    ensures
        result <= usize::BITS,
        value != 0 ==> result < usize::BITS,
;

proof fn lemma_transfer_multiset<T>(
    left: Multiset<T>,
    right: Multiset<T>,
    value: T,
)
    requires
        right.contains(value),
    ensures
        left.insert(value).add(right.remove(value)) == left.add(right),
{
    broadcast use vstd::multiset::group_multiset_axioms;
    assert(left.insert(value).add(right.remove(value)) =~= left.add(right));
}

fn source_vec_move_all<T, A: Allocator>(
    data: &mut Vec<T, A>,
    other: &mut Vec<T, A>,
)
    ensures
        final(data)@.to_multiset()
            == old(data)@.to_multiset().add(old(other)@.to_multiset()),
        final(data)@.len() == old(data)@.len() + old(other)@.len(),
        final(other)@ == Seq::<T>::empty(),
{
    let ghost combined = data@.to_multiset().add(other@.to_multiset());
    let ghost combined_len = data@.len() + other@.len();

    while !other.is_empty()
        invariant
            data@.to_multiset().add(other@.to_multiset()) == combined,
            data@.len() + other@.len() == combined_len,
        decreases other@.len(),
    {
        let ghost data_before = data@;
        let ghost other_before = other@;
        let value = other.remove(0);
        data.push(value);

        proof {
            broadcast use vstd::seq_lib::group_to_multiset_ensures;
            assert(other_before.to_multiset().contains(value));
            lemma_transfer_multiset(
                data_before.to_multiset(),
                other_before.to_multiset(),
                value,
            );
            assert(data@.to_multiset().add(other@.to_multiset()) == combined);
        }
    }

    proof {
        assert(other@.len() == 0);
        assert(other@ == Seq::<T>::empty());
        broadcast use vstd::multiset::group_multiset_axioms;
        broadcast use vstd::seq_lib::group_to_multiset_ensures;
        assert(data@.to_multiset() == combined);
    }
}

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
    if a < b {
        let ghost before = data@;
        let slice = data.as_mut_slice();
        let (left, right) = slice.split_at_mut(b);
        swap(&mut left[a], &mut right[0]);
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
        swap(&mut left[b], &mut right[0]);
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

fn source_sift_up<T: Ord, A: Allocator>(
    data: &mut Vec<T, A>,
    pos: usize,
) -> (result: usize)
    requires
        pos < old(data)@.len(),
    ensures
        result < final(data)@.len(),
        final(data)@.len() == old(data)@.len(),
        final(data)@.to_multiset() == old(data)@.to_multiset(),
{
    let mut hole_pos = pos;
    while hole_pos > 0
        invariant
            data@.len() == old(data)@.len(),
            data@.to_multiset() == old(data)@.to_multiset(),
            hole_pos < data@.len(),
        decreases hole_pos,
    {
        let parent = (hole_pos - 1) / 2;
        proof {
            assert(parent < hole_pos);
        }
        if data[hole_pos] <= data[parent] {
            break;
        }
        source_vec_swap(data, hole_pos, parent);
        hole_pos = parent;
    }
    hole_pos
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
        result < end,
        final(data)@.len() == old(data)@.len(),
        final(data)@.to_multiset() == old(data)@.to_multiset(),
{
    let mut hole_pos = pos;
    let mut child = hole_pos.wrapping_mul(2).wrapping_add(1);

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

fn source_rebuild<T: Ord, A: Allocator>(data: &mut Vec<T, A>)
    ensures
        final(data)@.len() == old(data)@.len(),
        final(data)@.to_multiset() == old(data)@.to_multiset(),
{
    let end = data.len();
    let mut n = end / 2;
    while n > 0
        invariant
            end == data@.len(),
            data@.len() == old(data)@.len(),
            data@.to_multiset() == old(data)@.to_multiset(),
            n <= end / 2,
        decreases n,
    {
        n -= 1;
        proof {
            assert(n < end);
        }
        source_sift_down_range(data, n, end);
    }
}

fn source_log2_fast(value: usize) -> (result: usize)
    requires
        value > 0,
{
    (usize::BITS - value.leading_zeros() - 1) as usize
}

fn source_rebuild_tail<T: Ord, A: Allocator>(
    data: &mut Vec<T, A>,
    start: usize,
)
    requires
        start <= old(data)@.len(),
    ensures
        final(data)@.len() == old(data)@.len(),
        final(data)@.to_multiset() == old(data)@.to_multiset(),
{
    if start == data.len() {
        return;
    }

    let end = data.len();
    let tail_len = end - start;

    let better_to_rebuild = if start < tail_len {
        true
    } else if end <= 2048 {
        end.wrapping_mul(2)
            < tail_len.wrapping_mul(source_log2_fast(start))
    } else {
        end.wrapping_mul(2) < tail_len.wrapping_mul(11)
    };

    if better_to_rebuild {
        source_rebuild(data);
    } else {
        let mut i = start;
        while i < end
            invariant
                end == data@.len(),
                data@.len() == old(data)@.len(),
                data@.to_multiset() == old(data)@.to_multiset(),
                start <= i <= end,
            decreases end - i,
        {
            source_sift_up(data, i);
            i += 1;
        }
    }
}

fn source_binary_heap_append<T: Ord, A: Allocator>(
    heap: &mut BinaryHeap<T, A>,
    other: &mut BinaryHeap<T, A>,
)
    ensures
        final(heap)@ == old(heap)@.add(old(other)@),
        final(other)@ == Multiset::<T>::empty(),
{
    let ghost heap_before = heap@;
    let ghost other_before = other@;

    if heap.len() < other.len() {
        swap(heap, other);
    }

    proof {
        broadcast use vstd::multiset::group_multiset_axioms;
        assert(heap@.add(other@) =~= heap_before.add(other_before));
    }
    let ghost combined = heap@.add(other@);

    {
        let data = unsafe { binary_heap_data_mut_rust_1_96(heap) };
        let other_data = unsafe { binary_heap_data_mut_rust_1_96(other) };
        let start = data.len();

        source_vec_move_all(data, other_data);

        proof {
            broadcast use vstd::multiset::group_multiset_axioms;
            broadcast use vstd::seq_lib::group_to_multiset_ensures;
            assert(data@.to_multiset() == combined);
            assert(other_data@.to_multiset() =~= Multiset::<T>::empty());
        }

        source_rebuild_tail(data, start);
    }
}

} // verus!

fn main() {}