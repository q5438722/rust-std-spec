#![feature(core_intrinsics)]
#![feature(nonzero_internals)]
#![allow(dead_code)]
#![allow(internal_features)]
#![allow(unused_imports)]

use core::num::{NonZero, ZeroablePrimitive};
use vstd::prelude::*;
use vstd::std_specs::nonzero::*;

verus! {

pub uninterp spec fn transmute_unchecked_relation<Src, Dst>(
    source: Src,
    destination: Dst,
) -> bool;

pub assume_specification<Src, Dst>[
    core::intrinsics::transmute_unchecked::<Src, Dst>
](source: Src) -> (destination: Dst)
    ensures
        transmute_unchecked_relation(source, destination),
    opens_invariants none
    no_unwind
;

pub axiom fn axiom_nonzero_transparent_encoding<T: ZeroablePrimitive>(
    source: NonZero<T>,
    destination: T,
)
    requires
        transmute_unchecked_relation(source, destination),
    ensures
        !destination.is_zero(),
        nonzero_from_primitive(destination) == source,
;

fn source_nonzero_get<T: ZeroablePrimitive>(
    n: NonZero<T>,
) -> (ret: T)
    ensures
        ret == n@,
    opens_invariants none
    no_unwind
{
    let ret = unsafe {
        core::intrinsics::transmute_unchecked(n)
    };
    proof {
        axiom_nonzero_transparent_encoding(n, ret);
        axiom_nonzero_from_primitive_view_eq(ret);
    }
    ret
}

}

fn main() {}