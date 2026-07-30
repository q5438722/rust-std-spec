#![allow(dead_code)]
#![allow(unused_imports)]

use core::mem;
use vstd::prelude::*;
use vstd::string::*;
use vstd::utf8::*;

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

pub axiom fn axiom_byte_slice_to_str_representation(
    source: &[u8],
    destination: &str,
)
    requires
        valid_utf8(source@),
        transmute_relation(source, destination),
    ensures
        destination@ == decode_utf8(source@),
;

pub const unsafe fn source_str_from_utf8_unchecked<'a>(
    v: &'a [u8],
) -> (res: &'a str)
    requires
        valid_utf8(v@),
    ensures
        res.spec_bytes() =~= v@,
{
    let res: &'a str = unsafe { mem::transmute(v) };
    proof {
        axiom_byte_slice_to_str_representation(v, res);
        decode_utf8_encode_utf8(v@);
    }
    res
}

} // verus!

fn main() {}