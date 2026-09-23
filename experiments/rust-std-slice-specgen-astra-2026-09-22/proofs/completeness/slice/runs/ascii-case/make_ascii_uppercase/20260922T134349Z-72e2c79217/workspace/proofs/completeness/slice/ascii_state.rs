use vstd::prelude::*;

#[path = "../../../specs/slice/ascii_post.rs"]
pub mod post;

verus! {

// The analysis input is only old(slice)@; its output is all of final(slice)@.
pub proof fn candidate_correspondence(slice: &mut [u8])
    ensures
        post::uppercase_post(old(slice)@, final(slice)@) <==> (
            final(slice)@ =~= old(slice)@.map_values(|byte: u8| post::uppercase_byte(byte))
        ),
        post::lowercase_post(old(slice)@, final(slice)@) <==> (
            final(slice)@ =~= old(slice)@.map_values(|byte: u8| post::lowercase_byte(byte))
        ),
{
}

pub proof fn lawful_outputs(initial: Seq<u8>)
    ensures
        post::uppercase_post(
            initial, initial.map_values(|byte: u8| post::uppercase_byte(byte)),
        ),
        post::lowercase_post(
            initial, initial.map_values(|byte: u8| post::lowercase_byte(byte)),
        ),
        initial.map_values(|byte: u8| post::uppercase_byte(byte)).len() == initial.len(),
        initial.map_values(|byte: u8| post::lowercase_byte(byte)).len() == initial.len(),
{
}

pub proof fn full_value_comparison(left: &[u8], right: &[u8])
    ensures
        (left =~= right) <==> (left@ =~= right@),
{
}

}
