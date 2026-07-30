#![allow(dead_code)]
#![allow(unused_imports)]

use std::vec::Vec;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

fn vec_default_proof<T>() -> (v: Vec<T>)
    ensures
        v@ == Seq::<T>::empty(),
{
    Vec::new()
}

}

fn main() {}