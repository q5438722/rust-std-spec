#![allow(dead_code, unused_imports, unused_variables)]
// Trusted-free source-transition model for core::slice::align_to.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct Input {
    pub source: Seq<int>,
    pub length: nat,
    pub address: nat,
    pub allocation: int,
    pub provenance: int,
    pub root_borrow: int,
    pub t_size: nat,
    pub u_size: nat,
    pub u_alignment: nat,
    pub usize_max: nat,
    pub outside_frame: Seq<int>,
}

pub ghost struct Boundary {
    pub initial_bytes: Seq<int>,
    pub address: nat,
    pub allocation: int,
    pub provenance: int,
    pub root_borrow: int,
    pub t_size: nat,
    pub u_size: nat,
    pub u_alignment: nat,
    pub outside_frame: Seq<int>,
}

pub ghost struct Output {
    pub branch: nat,
    pub offset: nat,
    pub prefix: Seq<int>,
    pub middle: Seq<int>,
    pub suffix: Seq<int>,
    pub prefix_length: nat,
    pub middle_length: nat,
    pub suffix_length: nat,
    pub prefix_address: nat,
    pub middle_address: nat,
    pub suffix_address: nat,
    pub prefix_allocation: int,
    pub middle_allocation: int,
    pub suffix_allocation: int,
    pub prefix_provenance: int,
    pub middle_provenance: int,
    pub suffix_provenance: int,
    pub prefix_borrow: int,
    pub middle_borrow: int,
    pub suffix_borrow: int,
    pub mutable: bool,
    pub disjoint: bool,
}

pub ghost struct FinalState {
    pub final_bytes: Seq<int>,
    pub final_source: Seq<int>,
    pub final_prefix: Seq<int>,
    pub final_middle: Seq<int>,
    pub final_suffix: Seq<int>,
    pub outside_final: Seq<int>,
}

pub open spec fn gcd(a: nat, c: nat) -> nat
    decreases c
{
    if c == 0 { a } else { gcd(c, a % c) }
}

pub open spec fn first_aligned_offset(
    address: nat,
    stride: nat,
    alignment: nat,
    address_space: nat,
    candidate: nat,
    remaining: nat,
) -> Option<nat>
    decreases remaining
{
    if remaining == 0 {
        None
    } else if ((address + candidate * stride) % address_space)
        % alignment == 0 {
        Some(candidate)
    } else {
        first_aligned_offset(
            address,
            stride,
            alignment,
            address_space,
            candidate + 1,
            (remaining - 1) as nat,
        )
    }
}

pub open spec fn align_offset(input: Input) -> nat {
    if input.t_size == 0 {
        if input.address % input.u_alignment == 0 {
            0
        } else {
            input.usize_max
        }
    } else {
        match first_aligned_offset(
            input.address,
            input.t_size,
            input.u_alignment,
            input.usize_max + 1,
            0,
            input.u_alignment,
        ) {
            Some(offset) => offset,
            None => input.usize_max,
        }
    }
}

pub open spec fn decode_word(
    bytes: Seq<int>,
    start: nat,
    size: nat,
) -> int
    decreases size
{
    if size == 0 {
        0
    } else {
        bytes[start as int]
            + 256 * decode_word(bytes, start + 1, (size - 1) as nat)
    }
}

pub open spec fn decode_elements(
    bytes: Seq<int>,
    start: nat,
    size: nat,
    count: nat,
) -> Seq<int>
    decreases count
{
    if count == 0 {
        Seq::empty()
    } else {
        seq![decode_word(bytes, start, size)]
            + decode_elements(
                bytes,
                start + size,
                size,
                (count - 1) as nat,
            )
    }
}

pub open spec fn source_output(input: Input, boundary: Boundary) -> Output {
    let zst = input.t_size == 0 || input.u_size == 0;
    let offset = if zst { 0 } else { align_offset(input) };
    let aligned = !zst && offset <= input.length;
    let prefix_length = if aligned { offset } else { input.length };
    let rest_length: nat = (input.length - prefix_length) as nat;
    let size_gcd = gcd(input.t_size, input.u_size);
    let ts: nat =
        if size_gcd == 0 { 1 }
        else { (input.u_size / size_gcd) as nat };
    let us: nat =
        if size_gcd == 0 { 0 }
        else { (input.t_size / size_gcd) as nat };
    let middle_length: nat =
        if aligned {
            ((rest_length / ts) * us) as nat
        } else {
            0
        };
    let suffix_length: nat =
        if aligned { (rest_length % ts) as nat } else { 0 };
    let prefix =
        if aligned {
            input.source.subrange(0, prefix_length as int)
        } else {
            input.source
        };
    let middle =
        if aligned {
            decode_elements(
                boundary.initial_bytes,
                prefix_length * input.t_size,
                input.u_size,
                middle_length,
            )
        } else {
            Seq::empty()
        };
    let suffix =
        if aligned {
            input.source.subrange(
                (input.length - suffix_length) as int,
                input.length as int,
            )
        } else {
            Seq::empty()
        };
    Output {
        branch: if zst { 0 }
            else if !aligned { 1 }
            else { 2 },
        offset,
        prefix,
        middle,
        suffix,
        prefix_length,
        middle_length,
        suffix_length,
        prefix_address: input.address,
        middle_address: input.address + prefix_length * input.t_size,
        suffix_address:
            input.address
                + ((input.length - suffix_length) as nat) * input.t_size,
        prefix_allocation: input.allocation,
        middle_allocation: if aligned { input.allocation } else { 0 },
        suffix_allocation: if aligned { input.allocation } else { 0 },
        prefix_provenance: input.provenance,
        middle_provenance: if aligned { input.provenance } else { 0 },
        suffix_provenance: if aligned { input.provenance } else { 0 },
        prefix_borrow: input.root_borrow,
        middle_borrow: if aligned { input.root_borrow } else { 0 },
        suffix_borrow: if aligned { input.root_borrow } else { 0 },
        mutable: false,
        disjoint: true,
    }
}

pub open spec fn source_state(
    input: Input,
    boundary: Boundary,
    final_bytes: Seq<int>,
) -> FinalState {
    let output = source_output(input, boundary);
    let final_source =
        decode_elements(final_bytes, 0, input.t_size, input.length);
    FinalState {
        final_bytes,
        final_source,
        final_prefix:
            if output.branch == 2 {
                decode_elements(
                    final_bytes,
                    0,
                    input.t_size,
                    output.prefix_length,
                )
            } else {
                final_source
            },
        final_middle:
            if output.branch == 2 {
                decode_elements(
                    final_bytes,
                    output.prefix_length * input.t_size,
                    input.u_size,
                    output.middle_length,
                )
            } else {
                Seq::empty()
            },
        final_suffix:
            if output.branch == 2 {
                decode_elements(
                    final_bytes,
                    ((input.length - output.suffix_length) as nat)
                        * input.t_size,
                    input.t_size,
                    output.suffix_length,
                )
            } else {
                Seq::empty()
            },
        outside_final: input.outside_frame,
    }
}

pub open spec fn boundary_holds(input: Input, boundary: Boundary) -> bool {
    boundary.address == input.address
        && boundary.allocation == input.allocation
        && boundary.provenance == input.provenance
        && boundary.root_borrow == input.root_borrow
        && boundary.t_size == input.t_size
        && boundary.u_size == input.u_size
        && boundary.u_alignment == input.u_alignment
        && boundary.outside_frame == input.outside_frame
}

pub open spec fn final_state_relation(
    input: Input,
    boundary: Boundary,
    state: FinalState,
) -> bool {
    state.final_bytes.len() == input.length * input.t_size
        && state == source_state(input, boundary, state.final_bytes)
        && (!false ==> state.final_bytes == boundary.initial_bytes)
}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {
    boundary_holds(input, boundary)
        && output == source_output(input, boundary)
        && final_state_relation(input, boundary, state)
}

pub proof fn exact_output_conditional_complete_align_to(
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
        output1 == output2,
{
    reveal(target_transition);
}


pub proof fn full_state_conditional_complete_align_to(
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
        output1 == output2,
        state1 == state2,
{
    reveal(target_transition);
    reveal(final_state_relation);
}


} // verus!
