use vstd::prelude::*;

#[path = "../../../specs/slice/split_off_post.rs"]
pub mod post;

verus! {

pub proof fn first_candidate_correspondence<'a, T>(
    slice: &mut &'a [T],
    result: Option<&'a T>,
)
    ensures
        post::split_off_first_post(
            (*old(slice))@,
            (
                match result {
                    None => None,
                    Some(value) => Some(*value),
                },
                (*final(slice))@,
            ),
        ) <==> match result {
            None => (*old(slice))@.len() == 0
                && (*final(slice))@ =~= (*old(slice))@,
            Some(value) => (*old(slice))@.len() > 0
                && *value == (*old(slice))@[0]
                && (*final(slice))@ =~=
                    (*old(slice))@.subrange(1, (*old(slice))@.len() as int),
        },
{
}

pub proof fn last_candidate_correspondence<'a, T>(
    slice: &mut &'a [T],
    result: Option<&'a T>,
)
    ensures
        post::split_off_last_post(
            (*old(slice))@,
            (
                match result {
                    None => None,
                    Some(value) => Some(*value),
                },
                (*final(slice))@,
            ),
        ) <==> match result {
            None => (*old(slice))@.len() == 0
                && (*final(slice))@ =~= (*old(slice))@,
            Some(value) => (*old(slice))@.len() > 0
                && *value == (*old(slice))@[(*old(slice))@.len() - 1]
                && (*final(slice))@ =~=
                    (*old(slice))@.subrange(0, (*old(slice))@.len() - 1),
        },
{
}

pub proof fn all_initial_states<T>(input_initial: Seq<T>)
    ensures
        post::split_off_first_post(input_initial, if input_initial.len() == 0 {
            (None, input_initial)
        } else {
            (Some(input_initial[0]), input_initial.subrange(1, input_initial.len() as int))
        }),
        post::split_off_last_post(input_initial, if input_initial.len() == 0 {
            (None, input_initial)
        } else {
            (Some(input_initial[input_initial.len() - 1]),
                input_initial.subrange(0, input_initial.len() - 1))
        }),
{
}

pub proof fn first_reconstruction<T>(
    input_initial: Seq<T>,
    observations: (Option<T>, Seq<T>),
)
    requires post::split_off_first_post(input_initial, observations),
    ensures
        observations.0.is_none() <==> input_initial.len() == 0,
        input_initial =~= match observations.0 {
            None => observations.1,
            Some(value) => seq![value] + observations.1,
        },
{
    if observations.0.is_some() {
        assert(input_initial =~=
            seq![input_initial[0]] + input_initial.subrange(1, input_initial.len() as int));
    }
}

pub proof fn last_reconstruction<T>(
    input_initial: Seq<T>,
    observations: (Option<T>, Seq<T>),
)
    requires post::split_off_last_post(input_initial, observations),
    ensures
        observations.0.is_none() <==> input_initial.len() == 0,
        input_initial =~= match observations.0 {
            None => observations.1,
            Some(value) => observations.1 + seq![value],
        },
{
    if observations.0.is_some() {
        assert(input_initial =~= input_initial.subrange(0, input_initial.len() - 1)
            + seq![input_initial[input_initial.len() - 1]]);
    }
}

pub proof fn complete_comparison<'a, T>(
    left: Option<&'a T>,
    right: Option<&'a T>,
    left_remaining: &[T],
    right_remaining: &[T],
)
    ensures
        (
            (((left is Some) == (right is Some))
                && ((left is Some) ==> (left->Some_0 == right->Some_0)))
            && (left_remaining =~= right_remaining)
        ) <==> (
            (
                match left { None => None, Some(value) => Some(*value) },
                left_remaining@,
            ) == (
                match right { None => None, Some(value) => Some(*value) },
                right_remaining@,
            )
        ),
{
}

}
