#![allow(dead_code)]
#![allow(unused_imports)]

use core::mem;
use vstd::prelude::*;
use vstd::string::*;

verus! {

pub uninterp spec fn transmute_relation<Src, Dst>(
    source: Src,
    destination: Dst,
) -> bool;

pub assume_specification<Src, Dst>[
    core::mem::transmute::<Src, Dst>
](source: Src) -> (destination: Dst)
    ensures
        transmute_relation(source, destination),
;

pub axiom fn axiom_str_to_byte_slice_representation(
    source: &str,
    destination: &[u8],
)
    requires
        transmute_relation(source, destination),
    ensures
        destination@ == source.spec_bytes(),
;

fn source_str_as_bytes(s: &str) -> (b: &[u8])
    ensures
        b@ == s.spec_bytes(),
{
    let b: &[u8] = unsafe { mem::transmute(s) };
    proof {
        axiom_str_to_byte_slice_representation(s, b);
    }
    b
}

} // verus!

fn main() {}