#![allow(dead_code, unused_imports, unused_variables)]
// Generated source-backed constructor model for core::slice::rchunks_mut.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct SliceIdentity {
    pub source: Seq<int>,
    pub start: int,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub borrow: int,
    pub element_size: nat,
}

pub open spec fn same_slice(left: SliceIdentity, right: SliceIdentity) -> bool {
    left.source == right.source
        && left.start == right.start
        && left.address == right.address
        && left.allocation == right.allocation
        && left.provenance == right.provenance
        && left.borrow == right.borrow
        && left.element_size == right.element_size
}

// Target proof prefix: rchunks_mut
pub ghost struct Input {
    pub slice: SliceIdentity,
    pub chunk_size: nat,
}

pub ghost struct RawSliceIdentity {
    pub address: int,
    pub length: nat,
    pub allocation: int,
    pub provenance: int,
}

pub ghost struct ChunkIterator {
    pub raw: RawSliceIdentity,
    pub marker_borrow: int,
    pub source: Seq<int>,
    pub remaining: Seq<int>,
    pub yielded_prefix: Seq<int>,
    pub remainder: Seq<int>,
    pub chunk_size: nat,
    pub reverse: bool,
    pub element_size: nat,
}

pub ghost struct FinalState {
    pub slice: SliceIdentity,
}

pub open spec fn mutable_raw_slice_cast(
    slice: SliceIdentity,
) -> RawSliceIdentity {
    RawSliceIdentity {
        address: slice.address,
        length: slice.source.len(),
        allocation: slice.allocation,
        provenance: slice.provenance,
    }
}

pub open spec fn output_transition(input: Input, iter: ChunkIterator) -> bool {
    iter.raw.address == input.slice.address
        && iter.raw.length == input.slice.source.len()
        && iter.raw.allocation == input.slice.allocation
        && iter.raw.provenance == input.slice.provenance
        && iter.marker_borrow == input.slice.borrow
        && iter.source == input.slice.source
        && iter.remaining == input.slice.source
        && iter.yielded_prefix == Seq::<int>::empty()
        && iter.remainder == Seq::<int>::empty()
        && iter.chunk_size == input.chunk_size
        && iter.reverse == true
        && iter.element_size == input.slice.element_size
}

pub open spec fn active_contract(input: Input, iter: ChunkIterator) -> bool {
    input.chunk_size > 0
        && iter.source == input.slice.source
        && iter.remaining == input.slice.source
        && iter.yielded_prefix == Seq::<int>::empty()
        && iter.remainder == Seq::<int>::empty()
        && iter.chunk_size == input.chunk_size
        && iter.reverse == true
}

pub open spec fn final_state_transition(
    input: Input,
    state: FinalState,
) -> bool {
    same_slice(state.slice, input.slice)
}

pub open spec fn target_transition(
    input: Input,
    iter: ChunkIterator,
    state: FinalState,
) -> bool {
    output_transition(input, iter)
        && active_contract(input, iter)
        && final_state_transition(input, state)
}

pub proof fn rchunks_mut_constructor(
    input: Input,
) -> (ret: ChunkIterator)
    requires
        input.chunk_size > 0,
    ensures
        output_transition(input, ret),
        active_contract(input, ret),
{
    let raw = mutable_raw_slice_cast(input.slice);
    ChunkIterator {
        raw,
        marker_borrow: input.slice.borrow,
        source: input.slice.source,
        remaining: input.slice.source,
        yielded_prefix: Seq::empty(),
        remainder: Seq::empty(),
        chunk_size: input.chunk_size,
        reverse: true,
        element_size: input.slice.element_size,
    }
}

pub open spec fn exact_equivalent(
    left: ChunkIterator,
    left_state: FinalState,
    right: ChunkIterator,
    right_state: FinalState,
) -> bool {
    left.raw.address == right.raw.address
        && left.raw.length == right.raw.length
        && left.raw.allocation == right.raw.allocation
        && left.raw.provenance == right.raw.provenance
        && left.marker_borrow == right.marker_borrow
        && left.source == right.source
        && left.remaining == right.remaining
        && left.yielded_prefix == right.yielded_prefix
        && left.remainder == right.remainder
        && left.chunk_size == right.chunk_size
        && left.reverse == right.reverse
        && left.element_size == right.element_size
        && same_slice(left_state.slice, right_state.slice)
}

pub proof fn conditional_complete_rchunks_mut(
    input: Input,
    iter1: ChunkIterator,
    state1: FinalState,
    iter2: ChunkIterator,
    state2: FinalState,
)
    requires
        target_transition(input, iter1, state1),
        target_transition(input, iter2, state2),
    ensures
        exact_equivalent(iter1, state1, iter2, state2),
{
    reveal(target_transition);
    reveal(output_transition);
    reveal(final_state_transition);
    reveal(exact_equivalent);
}

} // verus!
