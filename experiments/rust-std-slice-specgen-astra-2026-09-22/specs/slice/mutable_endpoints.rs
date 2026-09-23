use vstd::prelude::*;

verus! {

// Inputs are the original slice and the caller's final optional element.
// Outputs are the initial optional element and the entire returned slice.
pub open spec fn first_mut_post<T>(
    input_initial: Seq<T>,
    caller_final: Option<T>,
    observations: (Option<T>, Seq<T>),
) -> bool {
    match (observations.0, caller_final) {
        (None, None) => input_initial.len() == 0 && observations.1 =~= seq![],
        (Some(value), Some(written)) => {
            &&& input_initial.len() > 0
            &&& value == input_initial[0]
            &&& observations.1 == input_initial.update(0, written)
        },
        _ => false,
    }
}

pub open spec fn last_mut_post<T>(
    input_initial: Seq<T>,
    caller_final: Option<T>,
    observations: (Option<T>, Seq<T>),
) -> bool {
    match (observations.0, caller_final) {
        (None, None) => input_initial.len() == 0 && observations.1 =~= seq![],
        (Some(value), Some(written)) => {
            &&& input_initial.len() > 0
            &&& value == input_initial[input_initial.len() - 1]
            &&& observations.1 == input_initial.update(input_initial.len() - 1, written)
        },
        _ => false,
    }
}

}
