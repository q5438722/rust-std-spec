#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn source_option_as_mut<T>(option: &mut Option<T>) -> (res: Option<&mut T>)
    ensures
        (match *old(option) {
            None => final(option).is_none() && res.is_none(),
            Some(r) => final(option).is_some() && res.is_some() && *res.unwrap() == r
                && *final(res.unwrap()) == final(option).unwrap(),
        }),
{
    match *option {
        Some(ref mut x) => Some(x),
        None => None,
    }
}

} // verus!

fn main() {}