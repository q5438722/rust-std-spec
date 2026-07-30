#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::cmp::{PartialOrdIs, PartialOrdSpec};

verus! {

pub open spec fn adjacent_sorted<T: core::cmp::PartialOrd>(values: Seq<T>) -> bool {
    forall|i: int|
        i >= 0 && values.len() > i + 1 ==> (#[trigger] values[i]).is_le(&values[i + 1])
}

pub closed spec fn sorted_prefix<T: core::cmp::PartialOrd>(
    values: Seq<T>,
    end: int,
) -> bool {
    &&& 0 <= end < values.len()
    &&& forall|i: int|
        0 <= i < end ==> (#[trigger] values[i]).is_le(&values[i + 1])
}

proof fn lemma_unsorted_subrange<T: core::cmp::PartialOrd>(
    values: Seq<T>,
    start: int,
    end: int,
)
    requires
        0 <= start <= end <= values.len(),
        !adjacent_sorted(values.subrange(start, end)),
    ensures
        !adjacent_sorted(values),
{
    vstd::seq::lemma_seq_subrange_len(values, start, end);
    let part = values.subrange(start, end);
    let k = choose|k: int|
        k >= 0 && part.len() > k + 1
            && !(#[trigger] part[k]).is_le(&part[k + 1]);
    vstd::seq::lemma_seq_subrange_index(values, start, end, k);
    vstd::seq::lemma_seq_subrange_index(values, start, end, k + 1);
    assert(!adjacent_sorted(values)) by {
        assert(!values[start + k].is_le(&values[start + k + 1]));
    }
}

proof fn lemma_extend_sorted_prefix<T: core::cmp::PartialOrd>(
    values: Seq<T>,
    start: int,
    end: int,
)
    requires
        sorted_prefix(values, start),
        start < end <= values.len(),
        adjacent_sorted(values.subrange(start, end)),
    ensures
        sorted_prefix(values, end - 1),
{
    reveal(sorted_prefix);
    vstd::seq::lemma_seq_subrange_len(values, start, end);
    assert forall|j: int| 0 <= j < end - 1 implies
        (#[trigger] values[j]).is_le(&values[j + 1]) by {
        if j >= start {
            let k = j - start;
            vstd::seq::lemma_seq_subrange_index(values, start, end, k);
            vstd::seq::lemma_seq_subrange_index(values, start, end, k + 1);
        }
    }
}

proof fn lemma_prefix_and_tail_sorted<T: core::cmp::PartialOrd>(
    values: Seq<T>,
    start: int,
)
    requires
        sorted_prefix(values, start),
        adjacent_sorted(values.subrange(start, values.len() as int)),
    ensures
        adjacent_sorted(values),
{
    reveal(sorted_prefix);
    vstd::seq::lemma_seq_subrange_len(values, start, values.len() as int);
    assert forall|j: int| j >= 0 && values.len() > j + 1 implies
        (#[trigger] values[j]).is_le(&values[j + 1]) by {
        if j >= start {
            let k = j - start;
            vstd::seq::lemma_seq_subrange_index(
                values,
                start,
                values.len() as int,
                k,
            );
            vstd::seq::lemma_seq_subrange_index(
                values,
                start,
                values.len() as int,
                k + 1,
            );
        }
    }
}

// Mechanical expansion of `slice.windows(2).all(|w| w[0] <= w[1])`.
fn source_windows_2_all<T>(slice: &[T]) -> (ret: bool)
    where
        T: core::cmp::PartialOrd,
    requires
        T::obeys_partial_cmp_spec(),
    ensures
        ret <==> adjacent_sorted(slice@),
{
    proof {
        vstd::slice::axiom_spec_len(slice);
    }
    let mut rest = slice;
    let mut offset: usize = 0;
    while rest.len() >= 2
        invariant
            T::obeys_partial_cmp_spec(),
            offset <= slice@.len(),
            offset == 0 || offset < slice@.len(),
            rest@ == slice@.subrange(offset as int, slice@.len() as int),
            forall|j: int|
                0 <= j < offset ==> (#[trigger] slice@[j]).is_le(&slice@[j + 1]),
        decreases slice@.len() - offset,
    {
        proof {
            vstd::slice::axiom_spec_len(rest);
            assert(rest@.len() >= 2);
        }
        let ghost old_rest = rest@;
        let ghost old_offset = offset as int;
        let rest_len = rest.len();
        let window = &rest[0..2];
        let next_rest = &rest[1..rest_len];
        proof {
            vstd::seq::lemma_seq_subrange_len(
                slice@,
                old_offset,
                slice@.len() as int,
            );
            assert(old_rest.len() == slice@.len() - old_offset);
            assert(old_offset + 2 <= slice@.len());
            assert(vstd::slice::spec_slice_len(slice) <= usize::MAX);
            assert(slice@.len() == vstd::slice::spec_slice_len(slice));
            assert(slice@.len() <= usize::MAX);
            vstd::seq::lemma_seq_subrange_len(old_rest, 0, 2);
            vstd::slice::axiom_spec_len(window);
            assert(window@.len() == 2);
            vstd::seq::lemma_seq_subrange_len(
                slice@,
                old_offset,
                slice@.len() as int,
            );
            vstd::seq::lemma_seq_subrange_composition(
                slice@,
                old_offset,
                slice@.len() as int,
                0,
                2,
            );
            vstd::seq::lemma_seq_subrange_composition(
                slice@,
                old_offset,
                slice@.len() as int,
                1,
                old_rest.len() as int,
            );
            vstd::seq::lemma_seq_subrange_index(
                slice@,
                old_offset,
                old_offset + 2,
                0,
            );
            vstd::seq::lemma_seq_subrange_index(
                slice@,
                old_offset,
                old_offset + 2,
                1,
            );
            assert(window@[0] == slice@[old_offset]);
            assert(window@[1] == slice@[old_offset + 1]);
            assert(next_rest@ == slice@.subrange(old_offset + 1, slice@.len() as int));
        }
        rest = next_rest;
        let ordered = window[0] <= window[1];
        proof {
            assert(ordered <==> slice@[old_offset].is_le(&slice@[old_offset + 1]));
        }
        if !ordered {
            proof {
                assert(!adjacent_sorted(slice@)) by {
                    assert(!slice@[old_offset].is_le(&slice@[old_offset + 1]));
                }
            }
            return false;
        }
        proof {
            assert forall|j: int| 0 <= j < offset + 1 implies
                (#[trigger] slice@[j]).is_le(&slice@[j + 1]) by {
                if j >= offset {
                    assert(j == old_offset);
                }
            }
            assert(offset < usize::MAX);
        }
        offset += 1;
    }
    proof {
        assert(adjacent_sorted(slice@)) by {
            assert forall|j: int| j >= 0 && slice@.len() > j + 1 implies
                (#[trigger] slice@[j]).is_le(&slice@[j + 1]) by {
                assert(j < offset);
            }
        }
    }
    true
}

// Mechanical expansion of `slice.windows(2).fold(true, |acc, w| acc & (w[0] <= w[1]))`.
fn source_windows_2_fold<T>(slice: &[T]) -> (ret: bool)
    where
        T: core::cmp::PartialOrd,
    requires
        T::obeys_partial_cmp_spec(),
    ensures
        ret <==> adjacent_sorted(slice@),
{
    proof {
        vstd::slice::axiom_spec_len(slice);
    }
    let mut rest = slice;
    let mut offset: usize = 0;
    let mut accum = true;
    while rest.len() >= 2
        invariant
            T::obeys_partial_cmp_spec(),
            offset <= slice@.len(),
            offset == 0 || offset < slice@.len(),
            rest@ == slice@.subrange(offset as int, slice@.len() as int),
            accum <==> forall|j: int|
                0 <= j < offset ==> (#[trigger] slice@[j]).is_le(&slice@[j + 1]),
        decreases slice@.len() - offset,
    {
        proof {
            vstd::slice::axiom_spec_len(rest);
            assert(rest@.len() >= 2);
        }
        let ghost old_rest = rest@;
        let ghost old_offset = offset as int;
        let rest_len = rest.len();
        let window = &rest[0..2];
        let next_rest = &rest[1..rest_len];
        proof {
            vstd::seq::lemma_seq_subrange_len(
                slice@,
                old_offset,
                slice@.len() as int,
            );
            assert(old_rest.len() == slice@.len() - old_offset);
            assert(old_offset + 2 <= slice@.len());
            assert(vstd::slice::spec_slice_len(slice) <= usize::MAX);
            assert(slice@.len() == vstd::slice::spec_slice_len(slice));
            assert(slice@.len() <= usize::MAX);
            vstd::seq::lemma_seq_subrange_len(old_rest, 0, 2);
            vstd::slice::axiom_spec_len(window);
            assert(window@.len() == 2);
            vstd::seq::lemma_seq_subrange_len(
                slice@,
                old_offset,
                slice@.len() as int,
            );
            vstd::seq::lemma_seq_subrange_composition(
                slice@,
                old_offset,
                slice@.len() as int,
                0,
                2,
            );
            vstd::seq::lemma_seq_subrange_composition(
                slice@,
                old_offset,
                slice@.len() as int,
                1,
                old_rest.len() as int,
            );
            vstd::seq::lemma_seq_subrange_index(
                slice@,
                old_offset,
                old_offset + 2,
                0,
            );
            vstd::seq::lemma_seq_subrange_index(
                slice@,
                old_offset,
                old_offset + 2,
                1,
            );
            assert(window@[0] == slice@[old_offset]);
            assert(window@[1] == slice@[old_offset + 1]);
            assert(next_rest@ == slice@.subrange(old_offset + 1, slice@.len() as int));
        }
        rest = next_rest;
        let ordered = window[0] <= window[1];
        proof {
            assert(ordered <==> slice@[old_offset].is_le(&slice@[old_offset + 1]));
        }
        // Verus does not support boolean `&`; `ordered` was already evaluated.
        let ghost old_accum = accum;
        accum = if accum {
            ordered
        } else {
            false
        };
        proof {
            assert(accum <==> old_accum && ordered);
            assert(accum <==> forall|j: int|
                0 <= j < offset + 1
                    ==> (#[trigger] slice@[j]).is_le(&slice@[j + 1])) by {
                if accum {
                    assert forall|j: int| 0 <= j < offset + 1 implies
                        (#[trigger] slice@[j]).is_le(&slice@[j + 1]) by {
                        if j >= offset {
                            assert(j == old_offset);
                        }
                    }
                } else if forall|j: int|
                    0 <= j < offset + 1
                        ==> (#[trigger] slice@[j]).is_le(&slice@[j + 1])
                {
                    assert(old_accum);
                    assert(ordered);
                    assert(false);
                }
            }
            assert(offset < usize::MAX);
        }
        offset += 1;
    }
    proof {
        assert(accum <==> adjacent_sorted(slice@)) by {
            if accum {
                assert(adjacent_sorted(slice@)) by {
                    assert forall|j: int| j >= 0 && slice@.len() > j + 1 implies
                        (#[trigger] slice@[j]).is_le(&slice@[j + 1]) by {
                        assert(j < offset);
                    }
                }
            } else if adjacent_sorted(slice@) {
                assert forall|j: int| 0 <= j < offset implies
                    (#[trigger] slice@[j]).is_le(&slice@[j + 1]) by {
                    assert(offset > 0);
                    assert(offset < slice@.len());
                    assert(j + 1 < slice@.len());
                }
                assert(false);
            }
        }
    }
    accum
}

pub fn source_slice_is_sorted<T>(slice: &[T]) -> (ret: bool)
    where
        T: core::cmp::PartialOrd,
    requires
        T::obeys_partial_cmp_spec(),
    ensures
        ret <==> forall|i: int|
            i >= 0 && slice@.len() > i + 1 ==> (#[trigger] slice@[i]).is_le(&slice@[i + 1]),
{
    proof {
        vstd::slice::axiom_spec_len(slice);
    }
    // This odd number works the best. 32 + 1 extra due to overlapping chunk boundaries.
    const CHUNK_SIZE: usize = 33;
    if slice.len() < CHUNK_SIZE {
        return source_windows_2_all(slice);
    }
    let mut i = 0;
    proof {
        assert(sorted_prefix(slice@, 0)) by {
            reveal(sorted_prefix);
        }
    }
    // Check in chunks for autovectorization.
    while i < slice.len() - CHUNK_SIZE
        invariant
            T::obeys_partial_cmp_spec(),
            CHUNK_SIZE <= slice@.len(),
            sorted_prefix(slice@, i as int),
        decreases slice@.len() - i,
    {
        let chunk = &slice[i..i + CHUNK_SIZE];
        if !source_windows_2_fold(chunk) {
            proof {
                assert(!adjacent_sorted(chunk@));
                assert(chunk@ == slice@.subrange(i as int, (i + CHUNK_SIZE) as int));
                lemma_unsorted_subrange(
                    slice@,
                    i as int,
                    (i + CHUNK_SIZE) as int,
                );
            }
            return false;
        }
        proof {
            assert(adjacent_sorted(chunk@));
            assert(chunk@ == slice@.subrange(i as int, (i + CHUNK_SIZE) as int));
            lemma_extend_sorted_prefix(
                slice@,
                i as int,
                (i + CHUNK_SIZE) as int,
            );
        }
        // We need to ensure that chunk boundaries are also sorted.
        // Overlap the next chunk with the last element of our last chunk.
        i += CHUNK_SIZE - 1;
    }
    // Normalize the unsupported unbounded range end to the slice length.
    let tail_len = slice.len();
    let tail = &slice[i..tail_len];
    let result = source_windows_2_all(tail);
    proof {
        if result {
            assert(tail@ == slice@.subrange(i as int, slice@.len() as int));
            lemma_prefix_and_tail_sorted(slice@, i as int);
        } else {
            assert(tail@ == slice@.subrange(i as int, slice@.len() as int));
            lemma_unsorted_subrange(slice@, i as int, slice@.len() as int);
        }
    }
    result
}

} // verus!

fn main() {}