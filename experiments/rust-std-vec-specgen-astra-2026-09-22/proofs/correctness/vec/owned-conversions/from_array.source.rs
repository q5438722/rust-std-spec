#![cfg(not(no_global_oom_handling))]

use vstd::prelude::*;

verus! {

pub fn from_array<T, const N: usize>(s: [T; N]) -> (result: Vec<T>)
    ensures
        result@ == s@,
{
    <[T]>::into_vec(Box::new(s))
}

}
