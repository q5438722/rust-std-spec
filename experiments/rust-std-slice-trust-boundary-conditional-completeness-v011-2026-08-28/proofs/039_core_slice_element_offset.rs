use vstd::prelude::*;

verus! {

pub struct Input {
    pub receiver_length: int,
    pub subject_length: int,
    pub memory_token: int,
}

pub struct Boundary {
    pub receiver_address: int,
    pub subject_address: int,
    pub element_size: int,
    pub usize_max: int,
}

pub struct Output {
    pub tag: int,
    pub start: int,
    pub end: int,
}

pub struct FinalState {
    pub memory_token: int,
}

pub open spec fn source_output(
    input: Input,
    boundary: Boundary,
) -> Output {
    if boundary.element_size == 0 {
        Output { tag: 0, start: 0, end: 0 }
    } else {
        let modulus = boundary.usize_max + 1;
        let byte_offset =
            (boundary.subject_address - boundary.receiver_address) % modulus;
        if byte_offset % boundary.element_size != 0 {
            Output { tag: 1, start: 0, end: 0 }
        } else {
            let start = byte_offset / boundary.element_size;
            if start < input.receiver_length {
            Output { tag: 2, start, end: 0 }
        } else {
            Output { tag: 1, start: 0, end: 0 }
        }
        }
    }
}

pub open spec fn target_transition(
    input: Input,
    boundary: Boundary,
    output: Output,
    state: FinalState,
) -> bool {
    output.tag == source_output(input, boundary).tag
        && output.start == source_output(input, boundary).start
        && output.end == source_output(input, boundary).end
        && state.memory_token == input.memory_token
        && 1 >= 0
}

pub proof fn exact_output_conditional_complete(
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
        output1.tag == output2.tag,
        output1.start == output2.start,
        output1.end == output2.end,
{
    reveal(target_transition);
}

pub proof fn full_state_conditional_complete(
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
        output1.tag == output2.tag,
        output1.start == output2.start,
        output1.end == output2.end,
        state1.memory_token == state2.memory_token,
{
    reveal(target_transition);
}

}
