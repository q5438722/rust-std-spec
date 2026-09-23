use vstd::prelude::*;

#[path = "../specs/slice/raw.rs"]
mod bindings;

verus! {

// These clients use candidate bindings; they do not prove the array bodies.
pub fn shared_contents<T>(s: &T) -> (result: &[T])
    ensures
        result@ =~= seq![*s],
{
    core::slice::from_ref(s)
}

pub fn caller_selected_write<T>(s: &mut T, replacement: T)
    ensures
        *final(s) == replacement,
{
    let result = core::slice::from_mut(s);
    result[0] = replacement;
    let ghost written = result@;
    assert(written[0] == replacement);
    assert(written[0] == *s);
}

}
