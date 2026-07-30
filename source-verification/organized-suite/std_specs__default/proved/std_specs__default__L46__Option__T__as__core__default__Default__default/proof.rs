#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::std_specs::default::*;

verus! {

fn option_default_proof<T>() -> (r: Option<T>)
    ensures
        r == Option::<T>::None,
{
    proof {
        assert(Option::<T>::None == Option::<T>::None);
    }
    None
}

}

fn main() {}