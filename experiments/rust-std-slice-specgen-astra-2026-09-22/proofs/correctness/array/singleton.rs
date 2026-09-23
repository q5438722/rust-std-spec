use vstd::prelude::*;

#[path = "../../../specs/slice/raw_post.rs"]
mod contracts;

verus! {

// Rust 1.96 array/mod.rs:163-169.
pub const fn from_ref<T>(s: &T) -> (result: &[T; 1])
    ensures
        contracts::singleton_post(*s, result@),
{
    // SAFETY: Converting `&T` to `&[T; 1]` is sound.
    unsafe { &*(s as *const T).cast::<[T; 1]>() }
}

// Rust 1.96 array/mod.rs:171-177.
pub const fn from_mut<T>(s: &mut T) -> (result: &mut [T; 1])
    ensures
        contracts::singleton_post(*old(s), result@),
        contracts::singleton_post(*final(s), final(result)@),
{
    // SAFETY: Converting `&mut T` to `&mut [T; 1]` is sound.
    unsafe { &mut *(s as *mut T).cast::<[T; 1]>() }
}

}
