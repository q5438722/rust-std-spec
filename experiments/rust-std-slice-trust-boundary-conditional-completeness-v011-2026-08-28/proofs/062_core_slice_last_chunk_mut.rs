#![allow(dead_code, unused_imports, unused_variables)]
// Source-backed mutable fixed-chunk model for core::slice::last_chunk_mut.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct SliceIdentity {
    pub source: Seq<int>,
    pub start: int,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
}

pub ghost struct RegionIdentity {
    pub values: Seq<int>,
    pub start: int,
    pub length: int,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
    pub projection: int,
    pub unique: bool,
}

pub ghost struct RawPointerIdentity {
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
}

pub ghost struct ArrayPointerIdentity {
    pub raw: RawPointerIdentity,
    pub length: nat,
}

pub ghost struct Input {
    pub slice: SliceIdentity,
    pub n: nat,
}

pub ghost struct Boundary {
    pub input_address: int,
    pub input_allocation: int,
    pub input_provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
}

pub ghost struct Output {
    pub is_some: bool,
    pub split_index: int,
    pub tuple_array_position: int,
    pub array: RegionIdentity,
    pub other: RegionIdentity,
}

pub ghost struct FinalState {
    pub backing: SliceIdentity,
    pub prefix: RegionIdentity,
    pub suffix: RegionIdentity,
    pub composed_final: Seq<int>,
    pub unique_partition: bool,
    pub elements_unchanged: bool,
}

pub open spec fn empty_region() -> RegionIdentity {
    RegionIdentity {
        values: Seq::empty(),
        start: 0,
        length: 0,
        address: 0,
        allocation: 0,
        provenance: 0,
        parent_borrow: 0,
        element_size: 0,
        projection: 0,
        unique: false,
    }
}

pub open spec fn make_region(
    slice: SliceIdentity,
    offset: int,
    length: int,
    projection: int,
) -> RegionIdentity {
    RegionIdentity {
        values: slice.source.subrange(offset, offset + length),
        start: slice.start + offset,
        length,
        address: slice.address + offset * slice.element_size as int,
        allocation: slice.allocation,
        provenance: slice.provenance,
        parent_borrow: slice.parent_borrow,
        element_size: slice.element_size,
        projection,
        unique: true,
    }
}

pub open spec fn branch_succeeds(input: Input) -> bool {
    input.n <= input.slice.source.len()
}

pub open spec fn checked_sub_or_split_index(input: Input) -> int {
    if branch_succeeds(input) {
        input.slice.source.len() as int - input.n as int
    } else {
        -1
    }
}

pub open spec fn raw_parts_split(
    input: Input,
) -> (RegionIdentity, RegionIdentity) {
    let split = checked_sub_or_split_index(input);
    (
        make_region(input.slice, 0, split, 2),
        make_region(
            input.slice,
            split,
            input.slice.source.len() as int - split,
            2,
        ),
    )
}

pub open spec fn as_mut_ptr_transition(
    region: RegionIdentity,
) -> RawPointerIdentity {
    RawPointerIdentity {
        address: region.address,
        allocation: region.allocation,
        provenance: region.provenance,
        parent_borrow: region.parent_borrow,
        element_size: region.element_size,
    }
}

pub open spec fn cast_array_transition(
    raw: RawPointerIdentity,
    n: nat,
) -> ArrayPointerIdentity {
    ArrayPointerIdentity { raw, length: n }
}

pub open spec fn dereference_array_transition(
    region: RegionIdentity,
    ptr: ArrayPointerIdentity,
) -> RegionIdentity {
    RegionIdentity {
        values: region.values,
        start: region.start,
        length: ptr.length as int,
        address: ptr.raw.address,
        allocation: ptr.raw.allocation,
        provenance: ptr.raw.provenance,
        parent_borrow: ptr.raw.parent_borrow,
        element_size: ptr.raw.element_size,
        projection: 1,
        unique: true,
    }
}

pub open spec fn source_output(input: Input) -> Output {
    if branch_succeeds(input) {
        let pair = raw_parts_split(input);
        let prefix = pair.0;
        let suffix = pair.1;
        let array_region = if false { prefix } else { suffix };
        let raw = as_mut_ptr_transition(array_region);
        let array_ptr = cast_array_transition(raw, input.n);
        let array = dereference_array_transition(array_region, array_ptr);
        Output {
            is_some: true,
            split_index: checked_sub_or_split_index(input),
            tuple_array_position: 0,
            array,
            other: empty_region(),
        }
    } else {
        Output {
            is_some: false,
            split_index: -1,
            tuple_array_position: -1,
            array: empty_region(),
            other: empty_region(),
        }
    }
}

pub open spec fn source_state(input: Input) -> FinalState {
    if branch_succeeds(input) {
        let pair = raw_parts_split(input);
        FinalState {
            backing: input.slice,
            prefix: pair.0,
            suffix: pair.1,
            composed_final: input.slice.source,
            unique_partition: true,
            elements_unchanged: true,
        }
    } else {
        FinalState {
            backing: input.slice,
            prefix: empty_region(),
            suffix: empty_region(),
            composed_final: input.slice.source,
            unique_partition: true,
            elements_unchanged: true,
        }
    }
}

pub open spec fn boundary_holds(
    input: Input,
    boundary: Boundary,
) -> bool {
    boundary.input_address == input.slice.address
        && boundary.input_allocation == input.slice.allocation
        && boundary.input_provenance == input.slice.provenance
        && boundary.parent_borrow == input.slice.parent_borrow
        && boundary.element_size == input.slice.element_size
}

pub open spec fn active_contract(
    input: Input,
    output: Output,
    state: FinalState,
) -> bool {
    if branch_succeeds(input) {
        output.is_some
            && output.array.length == input.n as int
            && output.array.values
                == if false {
                    input.slice.source.subrange(0, input.n as int)
                } else {
                    input.slice.source.subrange(
                        input.slice.source.len() as int - input.n as int,
                        input.slice.source.len() as int,
                    )
                }
            && (!false || output.other.unique)
            && output.tuple_array_position == 0
            && state.backing.source == state.prefix.values + output.array.values
            && state.composed_final == state.backing.source
            && state.unique_partition
    } else {
        !output.is_some
            && state.backing.source == input.slice.source
            && state.composed_final == input.slice.source
    }
}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {
    boundary_holds(input, boundary)
        && output == source_output(input)
        && state == source_state(input)
        && active_contract(input, output, state)
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
        && left.projection == right.projection
        && left.unique == right.unique
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
        && left.parent_borrow == right.parent_borrow
        && left.element_size == right.element_size
}

pub open spec fn same_output(left: Output, right: Output) -> bool {
    left.is_some == right.is_some
        && left.split_index == right.split_index
        && left.tuple_array_position == right.tuple_array_position
        && same_region(left.array, right.array)
        && same_region(left.other, right.other)
}

pub open spec fn same_state(
    left: FinalState,
    right: FinalState,
) -> bool {
    same_slice(left.backing, right.backing)
        && same_region(left.prefix, right.prefix)
        && same_region(left.suffix, right.suffix)
        && left.composed_final == right.composed_final
        && left.unique_partition == right.unique_partition
        && left.elements_unchanged == right.elements_unchanged
}

pub proof fn conditional_complete_last_chunk_mut(
    input: Input,
    boundary: Boundary,
    output1: Output,
    state1: FinalState,
    output2: Output,
    state2: FinalState,
)
    requires
        target_transition(input, boundary, output1, state1),
        target_transition(input, boundary, output2, state2),
    ensures
        same_output(output1, output2),
        same_state(state1, state2),
{
    reveal(target_transition);
    reveal(same_output);
    reveal(same_state);
    reveal(same_region);
    reveal(same_slice);
}

pub proof fn conditional_complete_exact_output_last_chunk_mut(
    input: Input,
    boundary: Boundary,
    output1: Output,
    state1: FinalState,
    output2: Output,
    state2: FinalState,
)
    requires
        target_transition(input, boundary, output1, state1),
        target_transition(input, boundary, output2, state2),
    ensures
        same_output(output1, output2),
{
    reveal(target_transition);
    reveal(same_output);
    reveal(same_region);
}

} // verus!
