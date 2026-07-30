#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use core::slice;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

pub assume_specification<T>[ slice::from_ref::<T> ](value: &T) -> (res: &[T])
    ensures
        res@ == seq![*value],
;

fn source_option_as_slice<T>(option: &Option<T>) -> (res: &[T])
    ensures
        res@ == (match *option {
            Some(x) => seq![x],
            None => seq![],
        }),
{
    // These are exactly the two raw-parts cases justified in the Rust source.
    match option {
        Some(value) => slice::from_ref(value),
        None => &[],
    }
}

} // verus!

fn main() {}