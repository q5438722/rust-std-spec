use vstd::prelude::*;

#[path = "../../../../specs/slice/default_post.rs"]
mod contracts;
#[path = "../../../correctness/slice/default_mut.rs"]
mod source;

verus! {

fn observe<'a, T>(value: &'a mut [T]) -> (result: &'a [T])
    ensures
        result@ == old(value)@,
{
    &*value
}

proof fn full_value_comparison<T>(left: &[T], right: &[T])
    ensures
        (left =~= right) <==> (left@ =~= right@),
{
}

// S-MUT-RETURN: analysis only; the actual API still returns &'a mut [T].
pub fn default_mut_observation<'a, T>() -> (result: &'a [T])
    ensures
        contracts::default_post(result),
{
    observe(source::default_mut())
}

}
