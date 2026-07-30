#![allow(dead_code)]

use vstd::prelude::*;
use vstd::string::StringSliceAdditionalSpecFns;

verus! {

pub assume_specification[ <[u8]>::eq_ignore_ascii_case ](
    slice: &[u8],
    other: &[u8],
) -> (result: bool)
    ensures
        result == (
            slice@.len() == other@.len()
            && forall|i: int| i >= 0 && slice@.len() > i ==>
                (if slice@[i] >= 65 && 90 >= slice@[i] {
                    slice@[i] as int + 32
                } else {
                    slice@[i] as int
                }) == (if other@[i] >= 65 && 90 >= other@[i] {
                    other@[i] as int + 32
                } else {
                    other@[i] as int
                })
        ),
;

pub const fn source_core_str_eq_ignore_ascii_case(
    s: &str,
    other: &str,
) -> (res: bool)
    ensures
        res == (
            s.spec_bytes().len() == other.spec_bytes().len()
            && forall|i: int| i >= 0 && s.spec_bytes().len() > i ==>
                (if s.spec_bytes()[i] >= 65 && 90 >= s.spec_bytes()[i] {
                    s.spec_bytes()[i] as int + 32
                } else {
                    s.spec_bytes()[i] as int
                }) == (if other.spec_bytes()[i] >= 65 && 90 >= other.spec_bytes()[i] {
                    other.spec_bytes()[i] as int + 32
                } else {
                    other.spec_bytes()[i] as int
                })
        ),
{
    s.as_bytes().eq_ignore_ascii_case(other.as_bytes())
}

} // verus!

fn main() {}