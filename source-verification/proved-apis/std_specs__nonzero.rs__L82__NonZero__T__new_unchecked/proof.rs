#![feature(nonzero_internals)]
#![allow(dead_code)]
#![allow(unused_imports)]

use core::num::{NonZero, ZeroablePrimitive};
use vstd::prelude::*;
use vstd::std_specs::nonzero::*;

verus! {

unsafe fn source_nonzero_new_unchecked<T: ZeroablePrimitive>(
    n: T,
) -> (ret: NonZero<T>)
    requires
        !n.is_zero(),
    ensures
        ret@ == n,
    opens_invariants none
    no_unwind
{
    match NonZero::<T>::new(n) {
        Some(n) => n,
        None => {
            proof {
                assert(n.is_zero());
                assert(false);
            }
            vstd::pervasive::unreached()
        },
    }
}

} // verus!

fn main() {}