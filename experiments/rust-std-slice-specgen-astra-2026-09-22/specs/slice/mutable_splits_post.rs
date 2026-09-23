use vstd::prelude::*;

verus! {

pub open spec fn split_first_mut_post<T>(
    input_initial: Seq<T>,
    caller_final: Option<(T, Seq<T>)>,
    observations: (Option<(T, Seq<T>)>, Seq<T>),
) -> bool {
    match (observations.0, caller_final) {
        (None, None) => input_initial.len() == 0 && observations.1 =~= seq![],
        (Some((value, remainder)), Some((written, written_remainder))) => {
            &&& input_initial.len() > 0
            &&& value == input_initial[0]
            &&& remainder == input_initial.subrange(1, input_initial.len() as int)
            &&& written_remainder.len() == remainder.len()
            &&& observations.1 =~= seq![written] + written_remainder
        },
        _ => false,
    }
}

pub open spec fn split_last_mut_post<T>(
    input_initial: Seq<T>,
    caller_final: Option<(T, Seq<T>)>,
    observations: (Option<(T, Seq<T>)>, Seq<T>),
) -> bool {
    match (observations.0, caller_final) {
        (None, None) => input_initial.len() == 0 && observations.1 =~= seq![],
        (Some((value, remainder)), Some((written, written_remainder))) => {
            &&& input_initial.len() > 0
            &&& value == input_initial[input_initial.len() - 1]
            &&& remainder == input_initial.subrange(0, input_initial.len() - 1)
            &&& written_remainder.len() == remainder.len()
            &&& observations.1 =~= written_remainder + seq![written]
        },
        _ => false,
    }
}

}
