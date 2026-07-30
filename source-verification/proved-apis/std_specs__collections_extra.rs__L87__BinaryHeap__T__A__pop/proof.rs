#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::BinaryHeap;
use alloc::vec::Vec;
use core::alloc::Allocator;
use core::mem::swap;
use vstd::assert_seqs_equal;
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

pub assume_specification<T>[<[T]>::swap](
    slice: &mut [T],
    a: usize,
    b: usize,
)
    requires
        a < old(slice)@.len(),
        b < old(slice)@.len(),
    ensures
        final(slice)@.to_multiset() == old(slice)@.to_multiset(),
;

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

fn source_vec_take_last<T, A: Allocator>(
    data: &mut Vec<T, A>,
) -> (result: Option<T>)
    ensures
        old(data)@.len() > 0 ==> {
            &&& result == Some(old(data)@[old(data)@.len() - 1])
            &&& final(data)@ == old(data)@.subrange(0, old(data)@.len() - 1)
        },
        old(data)@.len() == 0 ==> {
            &&& result == None::<T>
            &&& final(data)@ == old(data)@
        },
{
    if data.is_empty() {
        None
    } else {
        let index = data.len() - 1;
        let value = data.remove(index);
        proof {
            lemma_remove_last(old(data)@);
        }
        Some(value)
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
        final(data)@.to_multiset() == old(data)@.to_multiset(),
        final(data)@.len() == old(data)@.len(),
{
    data.as_mut_slice().swap(a, b);
    proof {
        vstd::seq_lib::to_multiset_len(old(data)@);
        vstd::seq_lib::to_multiset_len(final(data)@);
    }
}

fn source_swap_item_with_zero<T, A: Allocator>(
    item: &mut T,
    data: &mut Vec<T, A>,
)
    requires
        old(data)@.len() > 0,
    ensures
        final(data)@.to_multiset().insert(*final(item))
            == old(data)@.to_multiset().insert(*old(item)),
        final(data)@.len() == old(data)@.len(),
{
    swap(item, &mut data[0]);
    proof {
        broadcast use vstd::multiset::group_multiset_axioms;
        broadcast use vstd::seq_lib::group_to_multiset_ensures;
        assert(final(data)@.to_multiset().insert(*final(item))
            =~= old(data)@.to_multiset().insert(*old(item)));
    }
}

fn source_sift_up<T: Ord, A: Allocator>(
    data: &mut Vec<T, A>,
    pos: usize,
)
    requires
        pos < old(data)@.len(),
    ensures
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
}

#[verifier::exec_allows_no_decreases_clause]
fn source_sift_down_to_bottom<T: Ord, A: Allocator>(
    data: &mut Vec<T, A>,
    pos: usize,
)
    requires
        pos < old(data)@.len(),
        pos == 0,
    ensures
        final(data)@.to_multiset() == old(data)@.to_multiset(),
{
    let end = data.len();
    let start = pos;
    let mut hole_pos = pos;
    let mut child = hole_pos.wrapping_mul(2).wrapping_add(1);

    while child < end.saturating_sub(1)
        invariant
            end == data@.len(),
            data@.len() == old(data)@.len(),
            data@.to_multiset() == old(data)@.to_multiset(),
            start < end,
            hole_pos < end,
    {
        proof {
            assert(child + 1 < end);
        }
        if data[child] <= data[child + 1] {
            child += 1;
        }
        source_vec_swap(data, hole_pos, child);
        hole_pos = child;
        child = hole_pos.wrapping_mul(2).wrapping_add(1);
    }

    if child == end - 1 {
        source_vec_swap(data, hole_pos, child);
        hole_pos = child;
    }

    source_sift_up(data, hole_pos);
}

proof fn lemma_pop_multiset<T>(s: Seq<T>)
    requires
        s.len() > 0,
    ensures
        s.to_multiset()
            == s.subrange(0, s.len() - 1).to_multiset().insert(s[s.len() - 1]),
{
    let prefix = s.subrange(0, s.len() - 1);
    assert_seqs_equal!(s, prefix.push(s[s.len() - 1]), i => {
        if i < s.len() - 1 {
            assert(prefix[i] == s[i]);
        } else {
            assert(i == s.len() - 1);
        }
    });
    vstd::seq_lib::to_multiset_build(prefix, s[s.len() - 1]);
}

proof fn lemma_remove_inserted<T>(m: Multiset<T>, value: T)
    ensures
        m.insert(value).contains(value),
        m.insert(value).remove(value) == m,
{
    broadcast use vstd::multiset::group_multiset_axioms;
    assert(m.insert(value).remove(value) =~= m);
}

fn source_binary_heap_pop<T: Ord, A: Allocator>(
    heap: &mut BinaryHeap<T, A>,
) -> (result: Option<T>)
    ensures
        match result {
            None => {
                &&& old(heap)@.len() == 0
                &&& final(heap)@ == old(heap)@
            },
            Some(value) => {
                &&& old(heap)@.contains(value)
                &&& final(heap)@ == old(heap)@.remove(value)
            },
        },
{
    let ghost heap_before = heap@;
    let data = unsafe { binary_heap_data_mut_rust_1_96(heap) };
    let ghost data_before = data@;

    match source_vec_take_last(data) {
        None => {
            proof {
                vstd::seq_lib::to_multiset_len(data_before);
                assert(heap_before.len() == 0);
                assert(data@.to_multiset() == heap_before);
            }
            None
        },
        Some(mut item) => {
            proof {
                lemma_pop_multiset(data_before);
                assert(heap_before == data@.to_multiset().insert(item));
            }

            if !data.is_empty() {
                source_swap_item_with_zero(&mut item, data);
                proof {
                    assert(heap_before == data@.to_multiset().insert(item));
                }
                source_sift_down_to_bottom(data, 0);
            }

            proof {
                assert(heap_before == data@.to_multiset().insert(item));
                lemma_remove_inserted(data@.to_multiset(), item);
                assert(heap_before.contains(item));
                assert(data@.to_multiset() == heap_before.remove(item));
            }
            Some(item)
        },
    }
}

}

fn main() {}