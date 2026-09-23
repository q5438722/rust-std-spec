use vstd::prelude::*;

#[path = "../../../specs/slice/raw_post.rs"]
mod contracts;
#[path = "../array/singleton.rs"]
mod array;

verus! {

// Rust 1.96 slice/raw.rs:198-205; array resolves to its source proof copy.
pub const fn from_ref<T>(s: &T) -> (result: &[T])
    ensures
        contracts::singleton_post(*s, result@),
{
    array::from_ref(s)
}

}
