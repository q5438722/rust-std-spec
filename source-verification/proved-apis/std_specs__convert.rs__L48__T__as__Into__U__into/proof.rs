#![allow(dead_code)]
#![allow(unused_imports)]

use core::convert::From;
use vstd::prelude::*;
use vstd::std_specs::convert::*;

verus! {

fn source_into<T, U: From<T>>(a: T) -> (ret: U)
    ensures
        call_ensures(U::from, (a,), ret),
{
    U::from(a)
}

} // verus!

fn main() {}