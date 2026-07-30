#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn source_option_is_none<T>(option: &Option<T>) -> (b: bool)
    ensures
        b == is_none(option),
    no_unwind
{
    !option.is_some()
}

}

fn main() {}