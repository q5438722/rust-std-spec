use vstd::prelude::*;

verus! {

pub const fn split_off_last<'a, T>(slice: &mut &'a [T]) -> Option<&'a T> {
    let Some((last, rem)) = slice.split_last() else { return None };
    *slice = rem;
    Some(last)
}

}
