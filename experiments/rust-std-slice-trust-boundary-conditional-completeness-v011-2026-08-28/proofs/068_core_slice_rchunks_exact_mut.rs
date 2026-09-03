#![allow(dead_code, unused_imports, unused_variables)]
// Generated source-backed exact-partition model for core::slice::rchunks_exact_mut.

use vstd::arithmetic::div_mod::*;
use vstd::arithmetic::mul::*;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::seq_lib::*;

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

pub ghost struct RegionIdentity {
    pub values: Seq<int>,
    pub start: int,
    pub length: nat,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
}

pub ghost struct RawSliceIdentity {
    pub address: int,
    pub length: nat,
    pub allocation: int,
    pub provenance: int,
}

pub ghost struct Input {
    pub slice: SliceIdentity,
    pub chunk_size: nat,
}

pub ghost struct ExactChunkIterator {
    pub source: SliceIdentity,
    pub remaining: RegionIdentity,
    pub yielded_prefix: Seq<int>,
    pub remainder: RegionIdentity,
    pub raw_v: RawSliceIdentity,
    pub marker_borrow: int,
    pub chunk_size: nat,
    pub reverse: bool,
    pub modulo_remainder: nat,
    pub split_index: nat,
}

pub ghost struct FinalState {
    pub backing: SliceIdentity,
    pub borrow_owned_by_iterator: bool,
    pub elements_unchanged: bool,
}

pub open spec fn make_region(
    slice: SliceIdentity,
    offset: nat,
    length: nat,
) -> RegionIdentity
    recommends
        offset + length <= slice.source.len(),
{
    RegionIdentity {
        values: slice.source.subrange(
            offset as int,
            (offset + length) as int,
        ),
        start: slice.start + offset as int,
        length,
        address: slice.address
            + (offset as int) * (slice.element_size as int),
        allocation: slice.allocation,
        provenance: slice.provenance,
        parent_borrow: slice.borrow,
        element_size: slice.element_size,
    }
}

pub open spec fn same_slice(
    left: SliceIdentity,
    right: SliceIdentity,
) -> bool {
    left.source == right.source
        && left.start == right.start
        && left.address == right.address
        && left.allocation == right.allocation
        && left.provenance == right.provenance
        && left.borrow == right.borrow
        && left.element_size == right.element_size
}

pub open spec fn same_region(
    left: RegionIdentity,
    right: RegionIdentity,
) -> bool {
    left.values == right.values
        && left.start == right.start
        && left.length == right.length
        && left.address == right.address
        && left.allocation == right.allocation
        && left.provenance == right.provenance
        && left.parent_borrow == right.parent_borrow
        && left.element_size == right.element_size
}

pub open spec fn same_raw(
    left: RawSliceIdentity,
    right: RawSliceIdentity,
) -> bool {
    left.address == right.address
        && left.length == right.length
        && left.allocation == right.allocation
        && left.provenance == right.provenance
}
pub open spec fn output_transition(
    input: Input,
    iter: ExactChunkIterator,
) -> bool {
    let n = input.slice.source.len();
    let rem = n % input.chunk_size;
    let split = rem;
    let remaining = make_region(
        input.slice,
        rem,
        (n - rem) as nat,
    );
    let remainder = make_region(
        input.slice,
        0,
        rem,
    );
    same_slice(iter.source, input.slice)
        && same_region(iter.remaining, remaining)
        && iter.yielded_prefix == Seq::<int>::empty()
        && same_region(iter.remainder, remainder)
        && iter.raw_v.address == remaining.address
        && iter.raw_v.length == remaining.length
        && iter.raw_v.allocation == remaining.allocation
        && iter.raw_v.provenance == remaining.provenance
        && iter.marker_borrow == input.slice.borrow
        && iter.chunk_size == input.chunk_size
        && iter.reverse == true
        && iter.modulo_remainder == rem
        && iter.split_index == split
}

pub open spec fn active_contract(
    input: Input,
    iter: ExactChunkIterator,
) -> bool {
    input.chunk_size > 0
        && iter.source.source == input.slice.source
        && iter.yielded_prefix == Seq::<int>::empty()
        && iter.chunk_size == input.chunk_size
        && iter.reverse == true
        && iter.remainder.length < iter.chunk_size
        && iter.remaining.length % iter.chunk_size == 0
        && iter.yielded_prefix.len() % iter.chunk_size == 0
        && iter.remainder.values + iter.remaining.values + iter.yielded_prefix == iter.source.source
}

pub open spec fn final_state_transition(
    input: Input,
    state: FinalState,
) -> bool {
    same_slice(state.backing, input.slice)
        && state.borrow_owned_by_iterator
        && state.elements_unchanged
}

pub open spec fn target_transition(
    input: Input,
    iter: ExactChunkIterator,
    state: FinalState,
) -> bool {
    input.chunk_size > 0
        && output_transition(input, iter)
        && active_contract(input, iter)
        && final_state_transition(input, state)
}

pub proof fn rchunks_exact_mut_constructor(
    input: Input,
) -> (ret: ExactChunkIterator)
    requires
        input.chunk_size > 0,
    ensures
        output_transition(input, ret),
        active_contract(input, ret),
{
    let n = input.slice.source.len();
    let rem = n % input.chunk_size;
    lemma_mod_decreases(n as nat, input.chunk_size as nat);
    assert(rem <= n);
    let split = rem;
    let remaining = make_region(
        input.slice,
        rem,
        (n - rem) as nat,
    );
    let remainder = make_region(
        input.slice,
        0,
        rem,
    );
    let ret = ExactChunkIterator {
        source: input.slice,
        remaining,
        yielded_prefix: Seq::empty(),
        remainder,
        raw_v: RawSliceIdentity {
            address: remaining.address,
            length: remaining.length,
            allocation: remaining.allocation,
            provenance: remaining.provenance,
        },
        marker_borrow: input.slice.borrow,
        chunk_size: input.chunk_size,
        reverse: true,
        modulo_remainder: rem,
        split_index: split,
    };
    let ni = n as int;
    let ci = input.chunk_size as int;
    lemma_mod_division_less_than_divisor(ni, ci);
    lemma_fundamental_div_mod(ni, ci);
    lemma_mod_multiples_basic(ni / ci, ci);
    lemma_mul_is_commutative(ci, ni / ci);
    assert((rem as int) == ni % ci);
    assert(ni == ci * (ni / ci) + (ni % ci));
    assert((((n - rem) as nat) as int) == ci * (ni / ci));
    assert(ci * (ni / ci) == (ni / ci) * ci);
    assert((((n - rem) as nat) as int) % ci == 0);
    input.slice.source.lemma_split_at(rem as int);
    assert(remainder.values + remaining.values == input.slice.source);
    assert(ret.remainder.length < ret.chunk_size);
    assert(ret.remaining.length % ret.chunk_size == 0);
    lemma_small_mod(0nat, input.chunk_size as nat);
    assert(ret.yielded_prefix.len() % ret.chunk_size == 0);
    assert(active_contract(input, ret));
    ret
}

pub open spec fn same_iterator(
    left: ExactChunkIterator,
    right: ExactChunkIterator,
) -> bool {
    same_slice(left.source, right.source)
        && same_region(left.remaining, right.remaining)
        && left.yielded_prefix == right.yielded_prefix
        && same_region(left.remainder, right.remainder)
        && same_raw(left.raw_v, right.raw_v)
        && left.marker_borrow == right.marker_borrow
        && left.chunk_size == right.chunk_size
        && left.reverse == right.reverse
        && left.modulo_remainder == right.modulo_remainder
        && left.split_index == right.split_index
}

pub open spec fn exact_equivalent(
    left: ExactChunkIterator,
    left_state: FinalState,
    right: ExactChunkIterator,
    right_state: FinalState,
) -> bool {
    same_iterator(left, right)
        && same_slice(left_state.backing, right_state.backing)
        && left_state.borrow_owned_by_iterator
            == right_state.borrow_owned_by_iterator
        && left_state.elements_unchanged == right_state.elements_unchanged
}

pub open spec fn exact_output_equivalent(
    left: ExactChunkIterator,
    right: ExactChunkIterator,
) -> bool {
    same_iterator(left, right)
}

pub proof fn conditional_complete_rchunks_exact_mut(
    input: Input,
    iter1: ExactChunkIterator,
    state1: FinalState,
    iter2: ExactChunkIterator,
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
    reveal(same_iterator);
    reveal(same_slice);
    reveal(same_region);
    reveal(same_raw);
}

pub proof fn conditional_complete_exact_output_rchunks_exact_mut(
    input: Input,
    iter1: ExactChunkIterator,
    state1: FinalState,
    iter2: ExactChunkIterator,
    state2: FinalState,
)
    requires
        target_transition(input, iter1, state1),
        target_transition(input, iter2, state2),
    ensures
        exact_output_equivalent(iter1, iter2),
{
    reveal(target_transition);
    reveal(output_transition);
    reveal(exact_output_equivalent);
    reveal(same_iterator);
    reveal(same_slice);
    reveal(same_region);
    reveal(same_raw);
}

} // verus!
