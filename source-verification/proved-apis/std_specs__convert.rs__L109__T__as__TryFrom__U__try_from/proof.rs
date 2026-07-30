#![allow(dead_code)]
#![allow(unused_imports)]

use core::convert::TryFrom;
use vstd::prelude::*;
use vstd::std_specs::convert::*;

verus! {

fn source_try_into<T, U: TryFrom<T>>(a: T) -> (ret: Result<U, U::Error>)
    ensures
        call_ensures(U::try_from, (a,), ret),
{
    U::try_from(a)
}

} // verus!

fn main() {}