#![allow(dead_code)]
#![allow(unused_imports)]

use std::vec::Vec;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

fn source_vec_default<T>() -> (v: Vec<T>)
    ensures
        v@ == Seq::<T>::empty(),
{
    Vec::new()
}

}

fn main() {}