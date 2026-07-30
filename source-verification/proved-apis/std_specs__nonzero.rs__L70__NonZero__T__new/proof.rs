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

pub axiom fn axiom_option_nonzero_niche_encoding<T: ZeroablePrimitive>(
    source: T,
    destination: Option<NonZero<T>>,
)
    requires
        transmute_unchecked_relation(source, destination),
    ensures
        match destination {
            Some(nz) => nz@ == source,
            None => source.is_zero(),
        },
;

fn source_nonzero_new<T: ZeroablePrimitive>(
    n: T,
) -> (ret: Option<NonZero<T>>)
    ensures
        match ret {
            Some(nz) => nz@ == n && !n.is_zero(),
            None => n.is_zero(),
        },
    opens_invariants none
    no_unwind
{
    let ret = unsafe {
        core::intrinsics::transmute_unchecked(n)
    };
    proof {
        axiom_option_nonzero_niche_encoding(n, ret);
        broadcast use group_nonzero_axioms;
    }
    ret
}

}

fn main() {}