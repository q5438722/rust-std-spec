use vstd::prelude::*;

#[path = "../../../specs/slice/mutable_splits_post.rs"]
pub mod post;

verus! {

pub proof fn first_candidate_correspondence<T>(
    slice: &mut [T],
    result: Option<(&mut T, &mut [T])>,
)
    ensures
        post::split_first_mut_post(
            old(slice)@,
            match result {
                None => None,
                Some((value, remainder)) => Some((*final(value), final(remainder)@)),
            },
            (
                match result {
                    None => None,
                    Some((value, remainder)) => Some((*value, remainder@)),
                },
                final(slice)@,
            ),
        ) <==> (
            (old(slice).len() == 0 ==> result.is_none() && final(slice)@ == seq![])
            && (old(slice).len() > 0 ==> (result matches Some((a, b))
                && *a == old(slice)[0]
                && b@ == old(slice)@[1..]
                && b@.len() == final(b)@.len()
                && final(slice)@ == seq![*final(a)] + final(b)@
            ))
        ),
{
}

pub proof fn last_candidate_correspondence<T>(
    slice: &mut [T],
    result: Option<(&mut T, &mut [T])>,
)
    ensures
        post::split_last_mut_post(
            old(slice)@,
            match result {
                None => None,
                Some((value, remainder)) => Some((*final(value), final(remainder)@)),
            },
            (
                match result {
                    None => None,
                    Some((value, remainder)) => Some((*value, remainder@)),
                },
                final(slice)@,
            ),
        ) <==> (
            (old(slice).len() == 0 ==> result.is_none() && final(slice)@ == seq![])
            && (old(slice).len() > 0 ==> (result matches Some((a, b))
                && *a == old(slice)@[old(slice).len() - 1]
                && b@ == old(slice)@[0..old(slice).len() - 1]
                && b@.len() == final(b)@.len()
                && final(slice)@ == final(b)@ + seq![*final(a)]
            ))
        ),
{
}

pub proof fn caller_domain<T>(
    input_initial: Seq<T>,
    caller_final: Option<(T, Seq<T>)>,
    observations: (Option<(T, Seq<T>)>, Seq<T>),
)
    requires
        post::split_first_mut_post(input_initial, caller_final, observations)
            || post::split_last_mut_post(input_initial, caller_final, observations),
    ensures
        match caller_final {
            None => input_initial.len() == 0,
            Some((_, written_remainder)) =>
                written_remainder.len() + 1 == input_initial.len(),
        },
        caller_final.is_none() <==> input_initial.len() == 0,
        observations.0.is_none() <==> caller_final.is_none(),
{
}

pub proof fn all_caller_writes<T>(
    input_initial: Seq<T>,
    caller_final: Option<(T, Seq<T>)>,
)
    requires
        match caller_final {
            None => input_initial.len() == 0,
            Some((_, written_remainder)) =>
                written_remainder.len() + 1 == input_initial.len(),
        },
    ensures
        post::split_first_mut_post(input_initial, caller_final, match caller_final {
            None => (None, seq![]),
            Some((written, written_remainder)) => (
                Some((input_initial[0], input_initial.subrange(1, input_initial.len() as int))),
                seq![written] + written_remainder,
            ),
        }),
        post::split_last_mut_post(input_initial, caller_final, match caller_final {
            None => (None, seq![]),
            Some((written, written_remainder)) => (
                Some((
                    input_initial[input_initial.len() - 1],
                    input_initial.subrange(0, input_initial.len() - 1),
                )),
                written_remainder + seq![written],
            ),
        }),
{
}

pub proof fn first_full_return<T>(
    input_initial: Seq<T>,
    caller_final: Option<(T, Seq<T>)>,
    observations: (Option<(T, Seq<T>)>, Seq<T>),
)
    requires
        post::split_first_mut_post(input_initial, caller_final, observations),
    ensures
        observations.1.len() == input_initial.len(),
        caller_final.is_some() ==> observations.1[0] == caller_final.unwrap().0,
        caller_final.is_some() ==> forall|i: int| 1 <= i < input_initial.len()
            ==> #[trigger] observations.1[i] == caller_final.unwrap().1[i - 1],
{
}

pub proof fn last_full_return<T>(
    input_initial: Seq<T>,
    caller_final: Option<(T, Seq<T>)>,
    observations: (Option<(T, Seq<T>)>, Seq<T>),
)
    requires
        post::split_last_mut_post(input_initial, caller_final, observations),
    ensures
        observations.1.len() == input_initial.len(),
        caller_final.is_some() ==>
            observations.1[input_initial.len() - 1] == caller_final.unwrap().0,
        caller_final.is_some() ==> forall|i: int| 0 <= i < input_initial.len() - 1
            ==> #[trigger] observations.1[i] == caller_final.unwrap().1[i],
{
}

pub proof fn value_state_comparison<T>(
    left: (Option<(T, Seq<T>)>, Seq<T>),
    right: (Option<(T, Seq<T>)>, Seq<T>),
)
    ensures
        (left == right) <==> (
            (match (left.0, right.0) {
                (None, None) => true,
                (Some((a, tail_a)), Some((b, tail_b))) => a == b && tail_a =~= tail_b,
                _ => false,
            })
            && left.1 =~= right.1
        ),
{
}

}
