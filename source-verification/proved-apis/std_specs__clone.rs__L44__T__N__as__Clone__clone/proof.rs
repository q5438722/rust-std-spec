#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::clone::*;
use core::clone::Clone;

verus! {

#[verifier::external_fn_specification]
pub fn ex_array_from_fn<T, const N: usize, F>(f: F) -> (res: [T; N])
where
    F: FnMut(usize) -> T,
    requires
        forall|i: int| 0 <= i < N ==> #[trigger] f.requires((i as usize,)),
    ensures
        forall|i: int| 0 <= i < N ==> f.ensures((i as usize,), res@[i]),
{
    core::array::from_fn(f)
}

fn source_array_clone<T: Clone, const N: usize>(a: &[T; N]) -> (res: [T; N])
    ensures
        forall|i| #![all_triggers] 0 <= i < N ==> cloned::<T>(a@[i], res@[i]),
        a@ =~= res@ ==> a@ == res@,
{
    // `from_trusted_iterator(a.iter().cloned())` ultimately fills indices in order.
    let f = |i: usize| -> (x: T)
        requires
            i < N,
        ensures
            cloned::<T>(a@[i as int], x),
    {
        a[i].clone()
    };
    core::array::from_fn(f)
}

}

fn main() {}