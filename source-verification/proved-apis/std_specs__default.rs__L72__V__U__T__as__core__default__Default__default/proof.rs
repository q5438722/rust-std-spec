#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::default::*;

verus! {

fn source_tuple3_default<
    V: core::default::Default,
    U: core::default::Default,
    T: core::default::Default,
>() -> (r: (V, U, T))
    ensures
        call_ensures(V::default, (), r.0),
        call_ensures(U::default, (), r.1),
        call_ensures(T::default, (), r.2),
{
    (
        {
            let x: V = Default::default();
            x
        },
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