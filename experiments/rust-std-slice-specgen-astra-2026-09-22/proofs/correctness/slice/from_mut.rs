use vstd::prelude::*;

#[path = "../../../specs/slice/raw_post.rs"]
mod contracts;
#[path = "../array/singleton.rs"]
mod array;

verus! {

// Rust 1.96 slice/raw.rs:207-213; array resolves to its source proof copy.
pub const fn from_mut<T>(s: &mut T) -> (result: &mut [T])
    ensures
        contracts::singleton_post(*old(s), result@),
        contracts::singleton_post(*final(s), final(result)@),
{
    array::from_mut(s)
}

}
