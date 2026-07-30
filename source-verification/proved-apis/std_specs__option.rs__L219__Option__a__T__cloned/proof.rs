#![allow(dead_code)]
#![allow(unused_imports)]

use core::clone::Clone;
use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn source_option_cloned<'a, T: Clone>(opt: Option<&'a T>) -> (res: Option<T>)
    ensures
        opt.is_none() ==> res.is_none(),
        opt.is_some() ==> res.is_some() && cloned::<T>(*opt.unwrap(), res.unwrap()),
{
    opt.map(T::clone)
}

} // verus!

fn main() {}