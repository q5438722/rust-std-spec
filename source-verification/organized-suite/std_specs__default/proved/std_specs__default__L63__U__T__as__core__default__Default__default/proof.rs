#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::default::*;

verus! {

fn tuple_default_proof<U: core::default::Default, T: core::default::Default>() -> (r: (U, T))
    ensures
        call_ensures(U::default, (), r.0),
        call_ensures(T::default, (), r.1),
{
    (
        {
            let x: U = Default::default();
            x
        },
        {
            let x: T = Default::default();
            x
        },
    )
}

} // verus!

fn main() {}