use vstd::prelude::*;

#[path = "../../../specs/slice/ascii_post.rs"]
mod contracts;

#[path = "../num/u8_ascii.rs"]
mod u8_ascii;

verus! {

// Rust 1.96 slice/ascii.rs:195-203; self is lifted to slice.
pub const fn make_ascii_lowercase(slice: &mut [u8])
    ensures
        contracts::lowercase_post(old(slice)@, final(slice)@),
{
    let mut i = 0;
    while i < slice.len()
        invariant
            i <= slice@.len(),
            slice@.len() == old(slice)@.len(),
            forall|j: int| 0 <= j < slice@.len() ==> #[trigger] slice@[j]
                == if j < i {
                    contracts::lowercase_byte(old(slice)@[j])
                } else {
                    old(slice)@[j]
                },
        decreases slice@.len() - i,
    {
        let byte = &mut slice[i];
        u8_ascii::make_ascii_lowercase(byte);
        i += 1;
    }
    proof {
        assert(slice@ =~= old(slice)@.map_values(|byte: u8| contracts::lowercase_byte(byte)));
    }
}

}
