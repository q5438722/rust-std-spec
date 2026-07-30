#![allow(dead_code)]

use vstd::prelude::*;

verus! {

pub assume_specification[ str::trim_end ](s: &str) -> (res: &str)
    ensures
        s@.len() >= res@.len(),
        res@ == s@.subrange(0, res@.len() as int),
;

pub fn source_core_str_trim_right(s: &str) -> (res: &str)
    ensures
        res@.is_prefix_of(s@),
{
    let res = s.trim_end();
    assert(res@.is_prefix_of(s@));
    res
}

} // verus!

fn main() {}