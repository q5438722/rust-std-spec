#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::string::*;
use vstd::utf8::*;

verus! {

pub assume_specification[ str::split_at_checked ](
    s: &str,
    mid: usize,
) -> (ret: Option<(&str, &str)>)
    ensures
        ret.is_some() <==> is_char_boundary(s.spec_bytes(), mid as int),
        ret.is_some() ==> ret.unwrap().0.spec_bytes()
            =~= s.spec_bytes().subrange(0, mid as int),
        ret.is_some() ==> ret.unwrap().1.spec_bytes()
            =~= s.spec_bytes().subrange(mid as int, s.spec_bytes().len() as int),
;

fn source_str_split_at(s: &str, mid: usize) -> (res: (&str, &str))
    requires
        is_char_boundary(s.spec_bytes(), mid as int),
    ensures
        res.0.spec_bytes() =~= s.spec_bytes().subrange(0, mid as int),
        res.1.spec_bytes()
            =~= s.spec_bytes().subrange(mid as int, s.spec_bytes().len() as int),
{
    match s.split_at_checked(mid) {
        None => {
            assert(false);
            vstd::vpanic!("byte index is not a char boundary")
        },
        Some(pair) => pair,
    }
}

} // verus!

fn main() {}