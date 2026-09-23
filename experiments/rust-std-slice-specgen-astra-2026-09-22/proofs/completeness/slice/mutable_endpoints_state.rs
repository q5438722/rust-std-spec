use vstd::prelude::*;

#[path = "../../../specs/slice/mutable_endpoints.rs"]
pub mod post;

verus! {

pub proof fn first_candidate_correspondence<T>(slice: &mut [T], result: Option<&mut T>)
    ensures
        post::first_mut_post(
            old(slice)@,
            match result { None => None, Some(value) => Some(*final(value)) },
            (match result { None => None, Some(value) => Some(*value) }, final(slice)@),
        ) <==> (
            (old(slice).len() == 0 ==> result.is_none() && final(slice)@ == seq![])
            && (old(slice).len() != 0 ==> result.is_some()
                && *result.unwrap() == old(slice)[0]
                && final(slice)@ == old(slice)@.update(0, *final(result.unwrap())))
        ),
{
}

pub proof fn last_candidate_correspondence<T>(slice: &mut [T], result: Option<&mut T>)
    ensures
        post::last_mut_post(
            old(slice)@,
            match result { None => None, Some(value) => Some(*final(value)) },
            (match result { None => None, Some(value) => Some(*value) }, final(slice)@),
        ) <==> (
            (old(slice).len() == 0 ==> result.is_none() && final(slice)@ == seq![])
            && (old(slice).len() != 0 ==> result.is_some()
                && *result.unwrap() == old(slice)@.last()
                && final(slice)@ == old(slice)@.update(
                    old(slice).len() - 1, *final(result.unwrap()),
                ))
        ),
{
}

pub proof fn caller_domain<T>(
    input_initial: Seq<T>,
    caller_final: Option<T>,
    observations: (Option<T>, Seq<T>),
)
    requires
        post::first_mut_post(input_initial, caller_final, observations)
            || post::last_mut_post(input_initial, caller_final, observations),
    ensures
        caller_final.is_none() <==> input_initial.len() == 0,
        observations.0.is_none() <==> caller_final.is_none(),
{
}

pub proof fn all_caller_writes<T>(input_initial: Seq<T>, caller_final: Option<T>)
    requires
        caller_final.is_none() <==> input_initial.len() == 0,
    ensures
        post::first_mut_post(input_initial, caller_final, match caller_final {
            None => (None, seq![]),
            Some(written) => (Some(input_initial[0]), input_initial.update(0, written)),
        }),
        post::last_mut_post(input_initial, caller_final, match caller_final {
            None => (None, seq![]),
            Some(written) => (
                Some(input_initial[input_initial.len() - 1]),
                input_initial.update(input_initial.len() - 1, written),
            ),
        }),
{
}

pub proof fn full_first_frame<T>(
    input_initial: Seq<T>,
    caller_final: Option<T>,
    observations: (Option<T>, Seq<T>),
)
    requires
        post::first_mut_post(input_initial, caller_final, observations),
    ensures
        observations.1.len() == input_initial.len(),
        forall|i: int| 0 <= i < input_initial.len() && i != 0
            ==> #[trigger] observations.1[i] == input_initial[i],
        caller_final.is_some() ==> observations.1[0] == caller_final.unwrap(),
{
}

pub proof fn full_last_frame<T>(
    input_initial: Seq<T>,
    caller_final: Option<T>,
    observations: (Option<T>, Seq<T>),
)
    requires
        post::last_mut_post(input_initial, caller_final, observations),
    ensures
        observations.1.len() == input_initial.len(),
        forall|i: int| 0 <= i < input_initial.len() && i != input_initial.len() - 1
            ==> #[trigger] observations.1[i] == input_initial[i],
        caller_final.is_some() ==>
            observations.1[input_initial.len() - 1] == caller_final.unwrap(),
{
}

pub proof fn value_state_comparison<T>(
    left: (Option<T>, Seq<T>),
    right: (Option<T>, Seq<T>),
)
    ensures
        (left == right) <==> (
            (match (left.0, right.0) {
                (None, None) => true,
                (Some(a), Some(b)) => a == b,
                _ => false,
            })
            && left.1 =~= right.1
        ),
{
}

}
