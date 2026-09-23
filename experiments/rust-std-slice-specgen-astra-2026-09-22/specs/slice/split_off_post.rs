use vstd::prelude::*;

verus! {

pub open spec fn split_off_first_post<T>(
    input_initial: Seq<T>,
    observations: (Option<T>, Seq<T>),
) -> bool {
    match observations.0 {
        None => input_initial.len() == 0 && observations.1 =~= input_initial,
        Some(value) => {
            &&& input_initial.len() > 0
            &&& value == input_initial[0]
            &&& observations.1 =~= input_initial.subrange(1, input_initial.len() as int)
        },
    }
}

pub open spec fn split_off_last_post<T>(
    input_initial: Seq<T>,
    observations: (Option<T>, Seq<T>),
) -> bool {
    match observations.0 {
        None => input_initial.len() == 0 && observations.1 =~= input_initial,
        Some(value) => {
            &&& input_initial.len() > 0
            &&& value == input_initial[input_initial.len() - 1]
            &&& observations.1 =~= input_initial.subrange(0, input_initial.len() - 1)
        },
    }
}

}
