#![allow(dead_code, unused_imports, unused_variables)]
// Source-backed mutable split model for core::slice::split_at_mut_checked.

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
    pub element_alignment: nat,
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
    pub element_alignment: nat,
    pub projection: int,
    pub unique: bool,
}

pub ghost struct PointerIdentity {
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
    pub element_alignment: nat,
}

pub ghost struct Input {
    pub slice: SliceIdentity,
    pub mid: nat,
}

pub ghost struct Boundary {
    pub input_address: int,
    pub input_allocation: int,
    pub input_provenance: int,
    pub parent_borrow: int,
    pub element_size: nat,
    pub element_alignment: nat,
}

pub ghost struct Output {
    pub has_pair: bool,
    pub split_index: int,
    pub left: RegionIdentity,
    pub right: RegionIdentity,
}

pub ghost struct FinalState {
    pub base_ptr: PointerIdentity,
    pub mid_ptr: PointerIdentity,
    pub tail_length: int,
    pub backing: SliceIdentity,
    pub left: RegionIdentity,
    pub right: RegionIdentity,
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
        element_alignment: 1,
        projection: 0,
        unique: false,
    }
}

pub open spec fn empty_pointer() -> PointerIdentity {
    PointerIdentity {
        address: 0,
        allocation: 0,
        provenance: 0,
        parent_borrow: 0,
        element_size: 0,
        element_alignment: 1,
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
        element_alignment: slice.element_alignment,
        projection,
        unique: true,
    }
}

pub open spec fn valid_input(input: Input) -> bool {
    true
}

pub open spec fn branch_succeeds(input: Input) -> bool {
    input.mid <= input.slice.source.len()
}

pub open spec fn as_mut_ptr_cast_transition(
    slice: SliceIdentity,
) -> PointerIdentity {
    PointerIdentity {
        address: slice.address,
        allocation: slice.allocation,
        provenance: slice.provenance,
        parent_borrow: slice.parent_borrow,
        element_size: slice.element_size,
        element_alignment: slice.element_alignment,
    }
}

pub open spec fn pointer_add_transition(
    ptr: PointerIdentity,
    count: nat,
) -> PointerIdentity {
    PointerIdentity {
        address: ptr.address + count as int * ptr.element_size as int,
        allocation: ptr.allocation,
        provenance: ptr.provenance,
        parent_borrow: ptr.parent_borrow,
        element_size: ptr.element_size,
        element_alignment: ptr.element_alignment,
    }
}

pub open spec fn unchecked_sub_transition(input: Input) -> int
    recommends input.mid <= input.slice.source.len()
{
    input.slice.source.len() as int - input.mid as int
}

pub open spec fn raw_slice_regions(
    input: Input,
) -> (RegionIdentity, RegionIdentity)
    recommends input.mid <= input.slice.source.len()
{
    (
        make_region(input.slice, 0, input.mid as int, 1),
        make_region(
            input.slice,
            input.mid as int,
            unchecked_sub_transition(input),
            2,
        ),
    )
}

pub open spec fn source_output(input: Input) -> Output {
    if branch_succeeds(input) {
        let regions = raw_slice_regions(input);
        Output {
            has_pair: true,
            split_index: input.mid as int,
            left: regions.0,
            right: regions.1,
        }
    } else {
        Output {
            has_pair: false,
            split_index: -1,
            left: empty_region(),
            right: empty_region(),
        }
    }
}

pub open spec fn source_state(input: Input) -> FinalState {
    if branch_succeeds(input) {
        let base_ptr = as_mut_ptr_cast_transition(input.slice);
        let mid_ptr = pointer_add_transition(base_ptr, input.mid);
        let regions = raw_slice_regions(input);
        FinalState {
            base_ptr,
            mid_ptr,
            tail_length: unchecked_sub_transition(input),
            backing: input.slice,
            left: regions.0,
            right: regions.1,
            composed_final: regions.0.values + regions.1.values,
            unique_partition: true,
            elements_unchanged: true,
        }
    } else {
        FinalState {
            base_ptr: empty_pointer(),
            mid_ptr: empty_pointer(),
            tail_length: -1,
            backing: input.slice,
            left: empty_region(),
            right: empty_region(),
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
        && boundary.element_alignment == input.slice.element_alignment
}

pub open spec fn active_contract(
    input: Input,
    output: Output,
    state: FinalState,
) -> bool {
    if branch_succeeds(input) {
        output.has_pair
            && output.left.values
                == input.slice.source.subrange(0, input.mid as int)
            && output.right.values
                == input.slice.source.subrange(
                    input.mid as int,
                    input.slice.source.len() as int,
                )
            && state.backing.source
                == output.left.values + output.right.values
            && state.composed_final == state.backing.source
    } else {
        !output.has_pair
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
    valid_input(input)
        && boundary_holds(input, boundary)
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
        && left.element_alignment == right.element_alignment
        && left.projection == right.projection
        && left.unique == right.unique
}

pub open spec fn same_pointer(
    left: PointerIdentity,
    right: PointerIdentity,
) -> bool {
    left.address == right.address
        && left.allocation == right.allocation
        && left.provenance == right.provenance
        && left.parent_borrow == right.parent_borrow
        && left.element_size == right.element_size
        && left.element_alignment == right.element_alignment
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
        && left.element_alignment == right.element_alignment
}

pub open spec fn same_output(left: Output, right: Output) -> bool {
    left.has_pair == right.has_pair
        && left.split_index == right.split_index
        && same_region(left.left, right.left)
        && same_region(left.right, right.right)
}

pub open spec fn same_state(
    left: FinalState,
    right: FinalState,
) -> bool {
    same_pointer(left.base_ptr, right.base_ptr)
        && same_pointer(left.mid_ptr, right.mid_ptr)
        && left.tail_length == right.tail_length
        && same_slice(left.backing, right.backing)
        && same_region(left.left, right.left)
        && same_region(left.right, right.right)
        && left.composed_final == right.composed_final
        && left.unique_partition == right.unique_partition
        && left.elements_unchanged == right.elements_unchanged
}

pub proof fn conditional_complete_split_at_mut_checked(
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
    reveal(same_pointer);
    reveal(same_slice);
}

pub proof fn conditional_complete_exact_output_split_at_mut_checked(
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
