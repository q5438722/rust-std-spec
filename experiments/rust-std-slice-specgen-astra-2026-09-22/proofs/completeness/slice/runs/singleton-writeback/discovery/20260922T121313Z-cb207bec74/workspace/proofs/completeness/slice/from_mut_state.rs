use vstd::prelude::*;

#[path = "../../../specs/slice/raw_post.rs"]
pub mod post;

verus! {

// Inputs: *old(s), final(result)@. Outputs: result@, *final(s).
pub open spec fn from_mut_post<T>(
    input_initial: T,
    caller_final: Seq<T>,
    observations: (Seq<T>, T),
) -> bool {
    &&& post::singleton_post(input_initial, observations.0)
    &&& post::singleton_post(observations.1, caller_final)
}

pub proof fn candidate_correspondence<T>(s: &mut T, result: &mut [T])
    ensures
        from_mut_post(*old(s), final(result)@, (old(result)@, *final(s)))
            <==> (
                post::singleton_post(*old(s), old(result)@)
                && post::singleton_post(*final(s), final(result)@)
            ),
{
}

pub proof fn caller_domain<T>(input_initial: T, tracked result: &&mut [T])
    requires
        post::singleton_post(input_initial, old(*result)@),
    ensures
        final(*result)@.len() == 1,
{
    vstd::slice::mut_ref_slice_len_eq(result);
}

pub proof fn all_caller_writes<T>(input_initial: T, caller_final: Seq<T>)
    requires
        caller_final.len() == 1,
    ensures
        from_mut_post(input_initial, caller_final, (seq![input_initial], caller_final[0])),
{
    assert(caller_final =~= seq![caller_final[0]]);
}

pub proof fn full_value_comparison<T>(
    left: &[T],
    right: &[T],
    left_returned: T,
    right_returned: T,
)
    ensures
        (left =~= right && left_returned == right_returned)
            <==> (left@ =~= right@ && left_returned == right_returned),
{
}

}
